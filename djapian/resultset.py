import xapian
import operator
from copy import deepcopy

from django.db.models import get_model

from djapian import utils, decider

class defaultdict(dict):
    def __init__(self, value_type):
        self._value_type= value_type

    def __getitem__(self, key):
        if key not in self:
            dict.__setitem__(self, key, list())
        return dict.__getitem__(self, key)

class ResultSet(object):
    def __init__(self, indexer, query_str, offset=0, limit=utils.DEFAULT_MAX_RESULTS,
                 order_by=None, prefetch=False, flags=None, stemming_lang=None,
                 filter=None, exclude=None, prefetch_select_related=False):
        self._indexer = indexer
        self._query_str = query_str
        self._offset = offset
        self._limit = limit
        self._order_by = order_by
        self._prefetch = prefetch
        self._prefetch_select_related = prefetch_select_related
        self._filter = filter or decider.X()
        self._exclude = exclude or decider.X()

        if flags is None:
            flags = xapian.QueryParser.FLAG_PHRASE\
                        | xapian.QueryParser.FLAG_BOOLEAN\
                        | xapian.QueryParser.FLAG_LOVEHATE
        self._flags = flags
        self._stemming_lang = stemming_lang

        self._resultset_cache = None
        self._mset = None
        self._query = None
        self._query_parser = None

    def spell_correction(self):
        return self._clone(
            flags=self._flags | xapian.QueryParser.FLAG_SPELLING_CORRECTION\
                                | xapian.QueryParser.FLAG_WILDCARD
        )

    def prefetch(self, select_related=False):
        return self._clone(
            prefetch=True,
            prefetch_select_related=select_related
        )

    def order_by(self, field):
        return self._clone(order_by=field)

    def flags(self, flags):
        return self._clone(flags=flags)

    def stemming(self, lang):
        return self._clone(stemming_lang=lang)

    def count(self):
        return self._clone()._do_count()

    def get_corrected_query_string(self):
        self._get_mset()
        return self._query_parser.get_corrected_query_string()

    def filter(self, *fields, **raw_fields):
        clone = self._clone()
        clone._add_filter_fields(fields, raw_fields)
        return clone

    def exclude(self, *fields, **raw_fields):
        clone = self._clone()
        clone._add_exclude_fields(fields, raw_fields)
        return clone

    # Private methods

    def _prepare_fields(self, fields=None, raw_fields=None):
        fields = fields and reduce(operator.and_, fields) or decider.X()

        if raw_fields:
            fields = fields & reduce(
                operator.and_,
                map(
                    lambda value: decider.X(**{value[0]: value[1]}),
                    raw_fields.iteritems()
                )
            )
        self._check_fields(fields)
        return fields

    def _add_filter_fields(self, fields=None, raw_fields=None):
        self._filter &= self._prepare_fields(fields, raw_fields)

    def _add_exclude_fields(self, fields=None, raw_fields=None):
        self._exclude &= self._prepare_fields(fields, raw_fields)

    def _check_fields(self, fields):
        known_fields = set([f.prefix for f in self._indexer.tags])

        for field in fields.children:
            if isinstance(field, decider.X):
                self._check_fields(field)
            else:
                if field[0].split('__', 1)[0] not in known_fields:
                    raise ValueError("Unknown field '%s'" % field[0])

    def _clone(self, **kwargs):
        data = {
            "indexer": self._indexer,
            "query_str": self._query_str,
            "offset": self._offset,
            "limit": self._limit,
            "order_by": self._order_by,
            "prefetch": self._prefetch,
            "prefetch_select_related": self._prefetch_select_related,
            "flags": self._flags,
            "stemming_lang": self._stemming_lang,
            "filter": deepcopy(self._filter),
            "exclude": deepcopy(self._exclude),
        }
        data.update(kwargs)

        return ResultSet(**data)

    def _do_count(self):
        self._get_mset()

        return self._mset.size()

    def _do_prefetch(self):
        model_map = defaultdict(list)

        for hit in self._resultset_cache:
            model_map[hit.model].append(hit)

        for model, hits in model_map.iteritems():
            pks = [hit.pk for hit in hits]

            instances = model._default_manager.all()

            if self._prefetch_select_related:
                instances = instances.select_related()

            instances = instances.in_bulk(pks)

            for hit in hits:
                hit.instance = instances[hit.pk]

    def _get_mset(self):
        if self._mset is None:
            self._mset, self._query, self._query_parser = self._indexer._do_search(
                self._query_str,
                self._offset,
                self._limit,
                self._order_by,
                self._flags,
                self._stemming_lang,
                self._filter,
                self._exclude,
            )

    def _fetch_results(self):
        if self._resultset_cache is None:
            self._get_mset()
            self._parse_results()

        return self._resultset_cache

    def _parse_results(self):
        self._resultset_cache = []

        for match in self._mset:
            doc = match.get_document()

            model = doc.get_value(2)
            model = get_model(*model.split('.'))
            pk = model._meta.pk.to_python(doc.get_value(1))

            percent = match.get_percent()
            rank = match.get_rank()
            weight = match.get_weight()

            tags = dict([(tag.prefix, tag.extract(doc))\
                                for tag in self._indexer.tags])

            self._resultset_cache.append(
                Hit(pk, model, percent, rank, weight, tags)
            )

        if self._prefetch:
            self._do_prefetch()

    def __iter__(self):
        self._fetch_results()
        return iter(self._resultset_cache)

    def __len__(self):
        self._fetch_results()
        return len(self._resultset_cache)

    def __getitem__(self, k):
        if not isinstance(k, (slice, int, long)):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0))
                or (isinstance(k, slice) and (k.start is None or k.start >= 0)
                    and (k.stop is None or k.stop >= 0))), \
                "Negative indexing is not supported."

        if self._resultset_cache is not None:
            return self._fetch_results()[k]
        else:
            if isinstance(k, slice):
                start, stop = k.start, k.stop
                if start is None:
                    start = 0
                if stop is None:
                    kstop = utils.DEFAULT_MAX_RESULTS

                return self._clone(
                    offset=start,
                    limit=stop - start
                )
            else:
                return list(self._clone(
                    offset=k,
                    limit=1
                ))[k]

        def __unicode__(self):
            return "<ResultSet: query=%s prefetch=%s>" % (self.query_str, self._prefetch)

class Hit(object):
    def __init__(self, pk, model, percent, rank, weight, tags):
        self.pk = pk
        self.model = model
        self.percent = percent
        self.rank = rank
        self.weight = weight
        self.tags = tags
        self._instance = None

    def get_instance(self):
        if self._instance is None:
            self._instance = self.model._default_manager.get(pk=self.pk)
        return self._instance

    def set_instance(self, instance):
        self._instance = instance

    instance = property(get_instance, set_instance)

    def __repr__(self):
        return "<Hit: model=%s pk=%s, percent=%s rank=%s weight=%s>" % (
            utils.model_name(self.model), self.pk, self.percent, self.rank, self.weight
        )
