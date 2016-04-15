from django.db import models
from datetime import datetime
# Create your models here.

class Ad(models.Model):
    ADS_STATUS_CHOICE = (
    (1,'LEFT SIDE BAR'),
    (2,'FOR VIEW STORE & VIEW ITEM'),
    (3,'BOTTOM PAGE ADS for every page except view_store&view_item'),
    )
    ad_name = models.CharField(max_length=50,blank=True)
    ad_image = models.ImageField(upload_to='ads/img', blank=True)
    ad_status = models.IntegerField(choices=ADS_STATUS_CHOICE,default=1)
    ad_website = models.URLField(blank=True,default='')
    date_added= models.DateTimeField(default=datetime.now,editable=False)
    date_rotation = models.DateTimeField(default=datetime.now)
    def __unicode__(self):
        return '%s' % (self.ad_name)

class AdForIndex(models.Model):
    ad_flash = models.ImageField(upload_to='ads/img', blank=True)
    ad_picture = models.ImageField(upload_to='ads/img', blank=True)
    ad_description = models.CharField(max_length=500,blank=True)
    date_added= models.DateTimeField(default=datetime.now,editable=False)
    def __unicode__(self):
        return '%s' % (self.ad_description)