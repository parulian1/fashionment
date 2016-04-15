from django.views.generic.simple import direct_to_template
from django.http import HttpResponse

def index(request):

    return direct_to_template(request,'base.html')

def force_error(request):
	if request.GET.get('doit'):
		raise Exception('force 500 raise exception error')
	return HttpResponse('no error YET')
