from coltrane.models import Category,FashionFacts
from django.views.generic.simple import direct_to_template
import datetime

from django.template import loader, RequestContext
from django.http import Http404, HttpResponse

def archive_index(request, queryset, date_field, num_latest=50,
        template_name=None, template_loader=loader,
        extra_context=None, allow_empty=True, context_processors=None,
        mimetype=None, allow_future=False, template_object_name='latest'):
    """
    Generic top-level archive of date-based objects.

    Templates: ``<app_label>/<model_name>_archive.html``
    Context:
        date_list
            List of years
        latest
            Latest N (defaults to 15) objects by date
    """
    if extra_context is None: extra_context = {}
    model = queryset.model
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: datetime.datetime.now()})
    date_list = queryset.dates(date_field, 'year')[::-1]
    if not date_list and not allow_empty:
        raise Http404, "No %s available" % model._meta.verbose_name

    if date_list and num_latest:
        latest = queryset.order_by('-'+date_field)[:num_latest]
    else:
        latest = None

    if not template_name:
        template_name = "%s/%s_archive.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'date_list' : date_list,
        template_object_name : latest,
    }, context_processors)
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    return HttpResponse(t.render(c), mimetype=mimetype)


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    fashion_fact = FashionFacts.objects.filter(categories=category.id)
    return direct_to_template(request,'coltrane/category_detail.html',
                                {
                                    'fashion_facts':fashion_fact,                                                                      
                                })

def cut(value, arg):
    "Removes all values of arg from the given string"
    return value.replace(arg, '')