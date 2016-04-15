from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _ 
#from markdown import markdown

class Magazine(models.Model):
    title = models.CharField(_('Title'),max_length=50, blank=True)
    description = models.CharField(_(u"Description"),max_length=500,blank=True)
    image=models.ImageField(_('Image'),upload_to='magazine/image/',blank=True)
    fact_img=models.ImageField(_('Image-2'),upload_to='magazine/image/',blank=True)
    url = models.URLField('URL',max_length=100,blank=True,verify_exists=False)
    download_file = models.FileField(upload_to='magazine/file/',blank=True)
    deleted= models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=datetime.now())
    def __unicode__(self):
        return unicode("%s: %s: %s image-1:%s , image2:%s" ) % (self.title,self.description,self.url,self.image,self.fact_img)