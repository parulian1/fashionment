from django.db import models

class FlashPageFlip(models.Model):
    ZIP_FILE = 1
    MANUAL = 2
    STATUS_DICT = {
        'zip':ZIP_FILE,
        'manual':MANUAL,
    }

    
    xml= models.FileField(upload_to='pageflip/')
    slug=models.SlugField()
    