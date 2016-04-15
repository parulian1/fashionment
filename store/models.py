from django.db import models
from accounts.models import User,ProvinceAreaCode,PhoneAreaCode,CountryAreaCode
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,date
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify,removetags,mark_safe
from store.postmarkup import render_bbcode

# Create your models here.
AVAILABILITY_CHOICE = (
(1,'In-Stock'),
(2,'Pre-Order'),
(3,'Sold Out'),
)
"""
GENDER_CHOICE = (
    (1,'MALE'),
    (0,'FEMALE'),
    )
"""
class Currency(models.Model):
    title = models.CharField(max_length=3)
    def __unicode__(self):
        return unicode('%s')%(self.title)

class LineCategory(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    
class Store(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=25)
    location = models.CharField(max_length=500,blank=True)
    province = models.ForeignKey(ProvinceAreaCode,blank=True,null=True)
    post_code = models.IntegerField()
    country = models.ForeignKey(CountryAreaCode,related_name='country_code')
    phone_area = models.ForeignKey(PhoneAreaCode,related_name='phone_code',blank=True,null=True)
    telephone=models.CharField(max_length=20)
    handphone=models.CharField(max_length=20,blank=True,null=True)
    fax_code = models.ForeignKey(PhoneAreaCode,related_name='fax_code' ,blank=True,null=True)
    fax=models.CharField(max_length=20,blank=True,null=True)
    company_website = models.URLField(blank=True)
#    contacts = models.CharField(max_length=20,blank=True)
#    email = models.CharField(max_length=50,blank=True)
    store_story = models.CharField(max_length=1000,blank=True)
    picture = models.ImageField(upload_to='store/img')
    promotion_text = models.CharField(max_length=1000,null=True)
    last_updated = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(unique=True,null=True,blank=True)
    deleted=models.BooleanField(default=False)
    def location_list(self):
        location_list=self.location.split('\r')
        return location_list
    def store_story_list(self):
        store_story_list=self.store_story.split('\r')
        return store_story_list
    def promotion_text_list(self):
        promotion_text_list=self.promotion_text.split('\r')
        return promotion_text_list
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('view_stores',args=(self.slug,))
#    def save(self):
#        super(Store,self).save()
#        new_line=Line(store=self,line=self.name+"'s line")
#        new_line.save()


class Line(models.Model):
    store = models.ForeignKey(Store,related_name='line_store')
    line = models.CharField(max_length=50)
    category = models.ForeignKey(LineCategory)
    slug = models.SlugField(null=True,blank=True)
    def __unicode__(self):
        return self.line
    
    def get_absolute_url(self):
        return reverse('view_line',args=(self.store.pk,))
    
    def save(self):
        self.slug=slugify(self.line)
        super(Line,self).save()

class Item(models.Model):
    IN_STOCK = 1
    PRE_ORDER = 2
    SOLD_OUT = 3
    MALE = 1
    FEMALE = 0
    UNISEX = 2
    AVAILABILITY_CHOICE = (
    (IN_STOCK,'In-Stock'),
    (PRE_ORDER,'Pre-Order'),
    (SOLD_OUT,'Sold Out')
    )
    GENDER_CHOICE = (
    (MALE,'MALE'),
    (FEMALE,'FEMALE'),
    (UNISEX,'UNISEX'),
    )
    line = models.ForeignKey(Line)
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,blank=True)
    colour = models.CharField(max_length=30,blank=True)
    size = models.CharField(max_length=30,blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICE,blank=True,null=True)
    currency = models.ForeignKey(Currency,null=True)
    price = models.IntegerField(max_length=9,default=0)
    #price_request = models.BooleanField(default=False,blank=True)
    availability = models.IntegerField(choices=AVAILABILITY_CHOICE,default=IN_STOCK)
    picture1 = models.ImageField(_(u"Picture1 (required)"),upload_to='cloth/img',null=True,help_text=_(u'2MB Upload Limit'))
    picture2 = models.ImageField(_(u"Picture2 (optional)"),upload_to='cloth/img', blank=True,null=True,help_text=_(u'2MB Upload Limit'))
    item_code =models.CharField(max_length=20,blank=True)
    deleted = models.BooleanField(default=False)
    last_updated = models.DateTimeField(default=datetime.now)
    primary = models.BooleanField(default=False)
    set_primary_date= models.DateTimeField(default=datetime.now,null=True)
    slug = models.SlugField(null=True,blank=True)
    def description_list(self):
        description_list=self.description.split('\r')
        return description_list
    def __unicode__(self):
        return self.item
    def get_absolute_url(self):
        return reverse('detail_items',args=(self.pk,self.slug))
    def get_previous_item(self):
        item_in_line = Item.objects.filter(line=self.line)
        counter = 0 # counter for checking item position
        previous = ''
        for item in item_in_line:
            if item.id == self.id:
                if counter>0:
                    previous = item_in_line[counter-1]
                else:
                    previous = None
            counter +=1
        return previous

    def get_next_item(self):
        item_in_line = Item.objects.filter(line=self.line).order_by('id')
        counter = 0 # counter for checking item position
        next = ''
        for item in item_in_line:
            if item.id == self.id:
                if counter<item_in_line.count()-1:
                    next = item_in_line[counter+1]
                else:
                    next = None
            counter +=1
        return next
    
    def save(self):
        if self.item!='' and self.item!=' ':
            self.slug=slugify(self.item[:50])
        else:
            self.slug = "no-name"
        super(Item,self).save()

class Addicted(models.Model):
    user = models.ForeignKey(User)
    store = models.ForeignKey(Store)
    deleted=models.BooleanField(default=False)
    class Meta:
        unique_together=(('user','store'),)
    def __unicode__(self):
        return '%s' % (self.store)
    
class Comment(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item,null=True)
    store = models.ForeignKey(Store,null=True)
    comment = models.TextField()
    date_added = models.DateTimeField(default=datetime.now())
    def save(self,force_insert=False, force_update=False):
        self.comment = removetags(self.comment,'script')
        self.comment = removetags(self.comment,'iframe')
        self.comment = render_bbcode(mark_safe(self.comment))
        super(Comment,self).save(force_insert=force_insert,force_update=force_update)
    def __unicode__(self):
        return '%s' %(self.user)

class View(models.Model):
    store = models.ForeignKey(Store,null=True)
    item = models.ForeignKey(Item,null=True)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s %s %s' %(self.store,self.item,self.count)

class CommentNumber(models.Model):
    store = models.ForeignKey(Store,null=True)
    item = models.ForeignKey(Item,null=True)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s %s %s' %(self.store,self.item,self.count)

class Rating(models.Model):
    store = models.ForeignKey(Store,null=True)
    item = models.ForeignKey(Item,null=True)
    avg_rate = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s %s' %(self.store,self.item)

class RatingCounter(models.Model):
    user = models.ForeignKey(User)
    store = models.ForeignKey(Store,null=True)
    item = models.ForeignKey(Item,null=True)
    rate = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=date.today())
    def __unicode__(self):
        return '%s %s %s' %(self.user,self.store,self.item)
        

class Compare_List(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together=(('user','item'),)
    def __unicode__(self):
        return '%s' %(self.item)
    
"""
class SearchFashionItemForm(ItemForm):
    category = forms.ModelChoiceField(Category.objects.all(),label=_(u'Category'))
    company_name = forms.ModelChoiceField(Store.objects.all(),label=_(u'Label'))
    class Meta(ItemForm.Meta):
        fields = [
                  'item',
                  'gender',
                  'category',
                  'company_name',
                  'availability',
                 ]
    def __init__(self, *args, **kwargs):
        super(SearchFashionItemForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = self.Meta.fields

"""        
