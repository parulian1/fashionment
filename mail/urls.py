from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns('',
    url(r'^compose/((?P<to_user>[-\w]+)/){0,1}$', 'mail.views.send_message',name='send_message'),
    url(r'^inbox/(?P<message_id>\d*)/*$', 'mail.views.inbox',name='inbox'),
    url(r'^send_items/(?P<message_id>\d*)/*$', 'mail.views.send_items',name='inbox2'),
    url(r'^draft/(?P<message_id>\d*)/*$', 'mail.views.draft',name='inbox3'),
    url(r'^notifications/(?P<message_id>\d*)/*$', 'mail.views.notifications',name='inbox4'),
    url(r'^message/complete/$','extra.views.result',{'template':'result.html','title':_('Your Message Has Been Sent'),}, name='message_complete'),
    #url(r'^complete/$','extra.views.result',{'template':'result.html','title':_('You successfully send a message'),}, name='msg_complete'),
    # ajax
    url(r'^lookup/$', 'mail.views.user_lookup',name='user_lookup'),
)
