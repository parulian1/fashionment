from django.core.management.base import BaseCommand
from store.models import Item
from django.template.defaultfilters import slugify

class Command(BaseCommand):
    def handle(self,*args,**options):
        items = Item.objects.all()
        for item in items:                     
            item.save()
        print "creating slug for each item success"