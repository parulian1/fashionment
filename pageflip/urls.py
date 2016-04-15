from django.conf.urls.defaults import *

urlpatterns = patterns('',    
    url(r'^swf/Pages.swf$', 'pageflip.views.test2'),
    #url(r'^add-file-zip/$', 'pageflip.views.add_file_zip',name='add_file_zip'),
    url(r'^add-file/(?P<type>[-\w]+)/$', 'pageflip.views.add_file_zip',name='add_pageflip'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'pageflip.views.test',name='test_pageflip'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/swf/Pages.swf$', 'pageflip.views.test2'),
    )