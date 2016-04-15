from django.db import models
from datetime import datetime
#from markdown import markdown

class Horoscope(models.Model):
    name = models.CharField(max_length=50)
    short_title = models.CharField(max_length = 70)
    description = models.TextField()
    show = models.BooleanField(default=False)
    artis_name = models.CharField(max_length=50,blank=True)
    artis_birthday = models.DateTimeField(default=datetime.today())
    artis_image = models.ImageField(upload_to='horoscope_artis/',blank=True)
    def __unicode__(self):
        return unicode("%s - %s") % (self.name,self.short_title) #to prevent coerce unicode error