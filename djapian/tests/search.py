from django.test import TestCase

from djapian.tests.utils import BaseTestCase, BaseIndexerTest, Entry, Person, Comment
from djapian.indexer import CompositeIndexer

class IndexerSearchTextTest(BaseIndexerTest, BaseTestCase):
    def setUp(self):
        super(IndexerSearchTextTest, self).setUp()
        self.result = Entry.indexer.search("text")

    def test_result_count(self):
        self.assertEqual(len(self.result), 3)

    def test_result_row(self):
        self.assertEqual(self.result[0].instance, self.entries[0])

    def test_result_list(self):
        self.assertEqual([r.instance for r in self.result], self.entries[0:3])

    def test_score(self):
        self.assert_(self.result[0].percent in (99, 100))

    def test_hit_fields(self):
        hit = self.result[0]

        self.assertEqual(hit.tags['title'], 'Test entry')

    def test_prefetch(self):
        result = self.result.prefetch()

        self.assertEqual(result[0].instance.author.name, 'Alex')

        result = self.result.prefetch(select_related=True)
        self.assert_(hasattr(result[0].instance, '_author_cache'))
        self.assertEqual(result[0].instance.author.name, 'Alex')

class AliasesTest(BaseTestCase):
    num_entries = 5

    def setUp(self):
        p = Person.objects.create(name="Alex")

        for i in range(self.num_entries):
            Entry.objects.create(author=p, title="Entry with number %s" % i, text="foobar " * i)

        Entry.indexer.update()

        self.result = Entry.indexer.search("subject:number")

    def test_result(self):
        self.assertEqual(len(self.result), self.num_entries)

class CorrectedQueryStringTest(BaseIndexerTest, BaseTestCase):
    def test_correction(self):
        results = Entry.indexer.search("texte").spell_correction()

        self.assertEqual(results.get_corrected_query_string(), "text")

class CompositeIndexerTest(BaseIndexerTest, BaseTestCase):
    def setUp(self):
        super(CompositeIndexerTest, self).setUp()
        self.indexer = CompositeIndexer(Entry.indexer, Comment.indexer)

    def test_search(self):
        results = self.indexer.search('entry')

        self.assertEqual(len(results), 4) # 3 entries + 1 comment
