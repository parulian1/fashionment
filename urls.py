from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from store import urls,views
from store.sitemap import StoreSitemap,ItemSitemap,LineSitemap
from coltrane.sitemap import ColtraneSitemap

admin.autodiscover()

sitemaps = {
    "store":StoreSitemap,
    "item": ItemSitemap,
    "line":LineSitemap,
    "Coltrane":ColtraneSitemap,
}
admin.site.index_template='admin/custom_index.html'
urlpatterns = patterns('',
    # Example:
    # (r'^fashion/', include('fashion.foo.urls')),
    #(r'^fashion/', include('clothing.urls')),
    #(r'^admin/', include(admin.urls),{'SSL':True}),
    
    (r'^account/', include('accounts.urls')),
    (r'^fashion/', include('store.urls')),
    (r'^fashion-facts/', include('coltrane.urls')),
    (r'^mail/', include('mail.urls')),
    (r'^contacts/', include('contacts.urls')),
    (r'^413/$','django.views.generic.simple.direct_to_template', {'template': '413.html'}),
    (r'^site-map/','django.views.generic.simple.direct_to_template', {'template': 'sitemap.html'}),
    (r'^rss/','django.views.generic.simple.direct_to_template', {'template': 'rss.xml'}),
    (r'^pageflip/', include('pageflip.urls')),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % settings.MEDIA_ROOT, 'show_indexes': True}),
    #(r'^(?P<slug>[-\w]*)/*$','django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'force-error', 'views.force_error'),
    
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {}, name='translation'),
    url(r'^google-results/search/','django.views.generic.simple.direct_to_template', {'template': 'google_results.html'},name="google_results"),
    url(r'^$','store.views.view_home',name='home'),
)
if settings.STATIC_MEDIA:
  #this line is so that production site does not serve static media with the line below, it is inefficient
  urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % settings.MEDIA_ROOT, 'show_indexes': True}),
  )
handler500='extra.views.server_error'
