from django.core.management.base import BaseCommand
from store.models import View
from django.template.defaultfilters import slugify

class Command(BaseCommand):
    def handle(self,*args,**options):
        views = View.objects.all().delete()
	
        print "reset view store,designer and item monthly success"