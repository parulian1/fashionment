import datetime
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from markdown import markdown
from tagging.models import Tag

STATUS_CHOICES = (
(1, 'Live'),
(2, 'Draft'),
(3, 'Hidden'),
)

class Category(models.Model):
    title = models.CharField(max_length = 250)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/fashion-facts/categories/%s/" % (self.slug)
    
#    def live_entry_set(self):
#        from coltrane.models import FashionFacts
#        return self.fashionfacts_set.filter(status=FashionFacts.LIVE_STATUS)

class FashionFacts(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS,'Draft'),
        (HIDDEN_STATUS, 'Hidden')
    )
    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    article_image=models.ImageField(upload_to='FashionFacts/img',blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    body_html = models.TextField(editable=False, blank=True)
    excerpt_html = models.TextField(editable=False, blank=True)

    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique_for_date='pub_date')
       
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    
    categories = models.ManyToManyField(Category)
    tags = TagField()

    def __unicode__(self):
        return self.title

    def save(self):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(FashionFacts, self).save()
        self.tag_list = self.tags
        
    def get_absolute_url(self):
        return "/fashion-facts/%s/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug, self.id)

    def get_absolute_url_year(self):
        return "/fashion-facts/%s/" % (self.pub_date.strftime("%Y"))
    def get_absolute_url_month(self):
        return "/fashion-facts/%s/" % (self.pub_date.strftime("%Y/%b").lower())
    def get_absolute_url_day(self):
        return "/fashion-facts/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower())

    def _get_tags(self):
        return Tag.objects.get_for_object(self)

    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)

    tag_list = property(_get_tags, _set_tags)
#class Link(models.Model):
#    title = models.CharField(max_length=250)
#    description = models.TextField(blank=True)
#    description_html = models.TextField(blank=True)
#    url = models.URLField(unique=True)
#    posted_by = models.ForeignKey(User)
#    pub_date = models.DateTimeField(default=datetime.datetime.now)
#    slug = models.SlugField(unique_for_date='pub_date')
#    tags = TagField()
#    enable_comments = models.BooleanField(default=True)
#    post_elsewhere= models.BooleanField('Post to del.icio.us', default=True)
#    via_name = models.CharField(max_length=250,blank=True)
#    via_url = models.URLField(blank=True)
#
#    def __unicode__(self):
#        return self.title
#
#    def save(self):
#        if self.description:
#            self.description_html = markdown(self.description)
#        super(link, self).save()


   
