from django.conf.urls.defaults import *
from django.template import RequestContext
from forms import ContactForm
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext 

urlpatterns = patterns('',
    #url(r'^$', ContactWizard([ContactOne, ContactTwo]),name="contacts"),
    #url(r'^$', index, name="contacts"),
    url(r'^$', 'contacts.views.index',name='contacts'),
    url(r'^complete/$','extra.views.result',{
    'title':_('Send Complete'),
    'template':'contacts/done.html',
    'description':_('E-mail have been send'),
    'links':[
      {
        'text':_('Kirim Lagi'),
        'reverse':{'name':'contacts'},
      },
    ]
    }, name='send_contact_complete'),
    #(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'contacts/contact.html','extra_context':{'form':ContactForm()}},'contacts'),
    (r'^done/$', 'django.views.generic.simple.direct_to_template', {'template': 'contacts/done.html'})
)
