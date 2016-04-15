from django.db import connection
from settings import DEBUG,MEDIA_URL
#TODO cannot use from django.conf import settings
#for some reason def query cannot see settings.DEBUG
def settings(request):
  return {'MEDIA_URL':MEDIA_URL}

def query(request):
  if DEBUG:
    query=connection.queries
  else:
    query=''
  return {'query':query}
  
def previous_url(request):
  return {'previous_url':request.META.get('HTTP_REFERER','/')}

def secure_url(request):
  from django.conf import settings
  if getattr(settings,'SSL',False) is True: 
    #if ssl exists and equals false
    return {'secure_url': 'https://%s%s' % (request.get_host(),request.get_full_path())}
  else:
    return {'secure_url': ''}

def use_google_analytics(request):
    return {'use_google_analytics':True}
def use_google_search(request):
    return {'use_google_search':True}