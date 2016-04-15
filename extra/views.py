from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import simplejson
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

def JsonResponse(request,json_dict={}):
  """
  if 'django.core.context_processors.auth' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
      raise ImproperlyConfigured("Put 'django.core.context_processors.auth' in your TEMPLATE_CONTEXT_PROCESSORS setting in order to use the admin application.")
  """

  if request.FILES:
    #cannot return json on upload but can return text string.
    #mimetype is text/html so that jquery AjaxForm can eval the string into json 
    return HttpResponse(simplejson.dumps(json_dict), mimetype='text/html')

  return HttpResponse(simplejson.dumps(json_dict), mimetype='application/javascript')

def result(request,title,links=[],template="extra/result.html",object_id=None,object_id2=None,description=''):
  reversed_links=[]
  for link in links:
    dictionary={'text':link['text']}
    if link['reverse'].get('args'):
      if type(link['reverse'].get('args')) is str:
        dictionary['url'] = reverse(link['reverse']['name'],args=(object_id,))
      else:
        dictionary['url'] = reverse(link['reverse']['name'],args=link['reverse']['args'])
    elif link['reverse'].has_key('arg_in_url'):
      dictionary['url'] = reverse(link['reverse']['name'],args=(object_id,))
    else:
      dictionary['url'] = reverse(link['reverse']['name'])
    reversed_links.append(dictionary)

  response_dict={
    'title':title,
    'links':reversed_links,
    'description':description,
  }

  if request.is_ajax():
    return JsonResponse(request,response_dict)

  return direct_to_template(request,template=template,extra_context=response_dict)

from django.conf import settings
from django import http
from django.template import Context, loader
def server_error(request, template_name='500.html',message=''):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'message': message,
        'MEDIA_URL': settings.MEDIA_URL
    })))
