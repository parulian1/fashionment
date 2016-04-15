from django.conf.urls.defaults import *
from coltrane.models import FashionFacts,Category
from magazine.models import Magazine
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from tagging.models import Tag
admin.autodiscover()

FashionFacts_info_dict = {
    'queryset': FashionFacts.objects.order_by('pub_date'),
    'date_field': 'pub_date',
    'template_object_name':'entry_list',
    'extra_context': { 'latest_entry': FashionFacts.objects.order_by('-pub_date'),
                        'our_magazines':Magazine.objects.filter(deleted=False).order_by('-date_added'),
    },
}
urlpatterns = patterns('',
    url(r'^tags/$','django.views.generic.list_detail.object_list',{ 'queryset': Tag.objects.all() },name='tag_page'),
    url(r'^tags/(?P<tag>[-\w]+)/$','tagging.views.tagged_object_list',{ 'queryset_or_model': FashionFacts,'template_name': 'tagging/entries_by_tag.html'},name='tag_view'),

)
urlpatterns += patterns('',
    url(r'^$', 'coltrane.views.archive_index', FashionFacts_info_dict,name='fashionfacts_archive_index'),
    url(r'^(?P<year>\d{4})/$','django.views.generic.date_based.archive_year',FashionFacts_info_dict,name='fashionfacts_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$','django.views.generic.date_based.archive_month',FashionFacts_info_dict,'fashionfacts_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$','django.views.generic.date_based.archive_day',FashionFacts_info_dict,'fashionfacts_archive_day'),
    #(r'^weblog/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$','coltrane.views.FashionFacts_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/(?P<object_id>\d+)/$','django.views.generic.date_based.object_detail', FashionFacts_info_dict,name='get_absolute_url'),
    
)
urlpatterns += patterns('',
    url(r'^categories/$','django.views.generic.list_detail.object_list',{ 'queryset': Category.objects.all() },name='category_list'),
    url(r'^categories/(?P<slug>[-\w]+)/$','coltrane.views.category_detail',name='category_detail'),
)

