from django.db.models import signals
from django.utils.functional import curry
from django.utils.decorators import decorator_from_middleware 

import registration

class CurrentUserMiddleware(object):
    def process_request(self, request):
        if request.method in ('GET','HEAD','OPTIONS','TRACE'):
            # This request shouldn't update anything,
            # so no signal handler should be attached.
            return

        if hasattr(request,'user') and request.user.is_authenticated():
            user = request.user
        else:
            user = None

        update_users = curry(self.update_users,user)
        signals.pre_save.connect(update_users, dispatch_uid=request, weak=False)

    def update_users(self,user,sender,instance,**kwargs):
        registry = registration.FieldRegistry()
        if sender in registry:
            for field in registry.get_fields(sender):
                setattr(instance, field.name, user)
            
    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid=request)
        return response

record_current_user = decorator_from_middleware(CurrentUserMiddleware)

__license__ = "Python"
__copyright__ = "Copyright (C) 2007, Stephen Zabel"
__author__ = "Stephen Zabel - sjzabel@gmail.com"
__contributors__ = "Jay Parlar - parlar@gmail.com"

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, get_host

SSL = 'SSL'

class SSLRedirect:
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        else:
            secure = False

        if (not secure == self._is_secure(request)) and getattr(settings,'SSL',False) is True:
            return self._redirect(request, secure)

    def _is_secure(self, request):
        if request.is_secure():
          return True

        #Handle the Webfaction case until this gets resolved in the request.is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

        return False

    def _redirect(self, request, secure):
        protocol = secure and "https" or "http"
        newurl = "%s://%s%s" % (protocol,get_host(request),request.get_full_path())
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError, \
        """Django can't perform a SSL redirect while maintaining POST data.
           Please structure your views so that redirects only occur during GETs."""

        return HttpResponsePermanentRedirect(newurl)

class FileAjaxRequest(object):
    def process_request(self,request):
        default_is_ajax = request.is_ajax()
        is_file_ajax = request.POST.has_key('file_ajax')

        request.is_file_ajax = lambda : is_file_ajax and request.FILES 
        request.is_ajax = lambda : default_is_ajax or is_file_ajax

class ReCaptchaMiddleware(CurrentUserMiddleware):
    """
    A tiny middleware to automatically add IP address to ReCaptcha
    POST requests
    """
    def process_request(self, request):
        """
        super(ReCaptchaMiddleware,self).process_request(request)
        """
        if request.method == 'POST' and 'recaptcha_challenge_field' in request.POST and 'recaptcha_ip_field' not in request.POST:
            data = request.POST.copy()
            data['recaptcha_ip_field'] = request.META['REMOTE_ADDR']
            request.POST = data

    def update_users(self,user,sender,instance,**kwargs):
        registry = registration.FieldRegistry()

        #raise Exception('x')
        if sender in registry:
            for field in registry.get_fields(sender):
                raise Exception(field)
                setattr(instance, field.name, user)

    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid=request)
        return response

#from signals import taster

#def my_handler(a,**kwargs):
#    a.stop = True
#    raise Exception('boo')
#taster.connect(my_handler)
