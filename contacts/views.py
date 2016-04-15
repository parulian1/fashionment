# Create your views here.
"""
from django.shortcuts import render_to_response , get_object_or_404
from django import newforms as forms
from django.template import RequestContext
from contacts.forms import ContactOne
def test(request):
  f=ContactOne
#  return HttpResponse('contanct test')
  return render_to_response('contacts/contact.html',{'forms':f},context_instance=RequestContext(request))
"""
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from forms import ContactForm
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
  if request.POST:
    form=ContactForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('send_contact_complete'))
  else:
    form=ContactForm()
  return direct_to_template(request,'contacts/contact.html',{'form':form})
