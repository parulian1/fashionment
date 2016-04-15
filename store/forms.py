from accounts.models import CountryAreaCode,ProvinceAreaCode,PhoneAreaCode
from django import forms
from django.utils.translation import ugettext_lazy as _
from extra.fields import ModelFkChoiceField
import re
from store.models import Comment,Item,Line,LineCategory,Store,Currency
from store.index import store_indexers
from django.conf import settings
from django.template.defaultfilters import filesizeformat

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class StoreForm(forms.ModelForm):
    country = forms.ModelChoiceField(CountryAreaCode.objects.order_by('country_name'))
    province = ModelFkChoiceField(ProvinceAreaCode.objects.order_by('province_name'),fk='country_id',required=False)
    phone_area = ModelFkChoiceField(PhoneAreaCode.objects.order_by('code'),fk='prov_id',required=False)
    fax_code = ModelFkChoiceField(PhoneAreaCode.objects.order_by('code'),fk='prov_id',required=False)
    store_story = forms.CharField(help_text=_(u'Max length is 1000 character'),widget=forms.Textarea(attrs={'maxlength':1000,'rows':5}))
    picture = forms.ImageField(help_text=_(u'2MB Upload Limit'))
    company_website = forms.URLField(required=False,help_text='http://example.com/')
    location = forms.CharField(help_text=_(u'Max length is 100 character'),widget=forms.Textarea(attrs={'maxlength':100,'rows':5}))
    promotion_text = forms.CharField(help_text=_(u'Max length is 1000 character'),widget=forms.Textarea(attrs={'maxlength':1000,'rows':5}),required=False)
    checkbox = forms.BooleanField(required=False,help_text=_(u'Tick this to fill in * fields to be same as profile'))
    class Meta:
        model=Store
        fields=[
        'name',
        'checkbox',
        'location',
        'country',
        'province',
        'post_code',
        'phone_area',
        'telephone',
        'handphone',
        'fax_code',
        'fax',
        'company_website',
        'store_story',
        'picture',
        'promotion_text',
#          'last_updated',
        ]
    def __init__(self, *args, **kwargs):
      super(StoreForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields
      
    def clean_name(self):
        name = self.cleaned_data.get('name')
        store = Store.objects.filter(name=name,deleted=False)
        if store:
            raise forms.ValidationError(_(u"Store name had been used by someone else."))
        return name
    
    def clean_province(self):
        country = self.cleaned_data.get('country')
        province = self.cleaned_data.get('province')
        if country=="1":
            if not province:
                raise forms.ValidationError(_(u"Please choose your province"))
            else:
                return province
    def clean_location(self):
        location=self.cleaned_data.get('location')
        if len(location) > 100:
            raise forms.ValidationError(_(u"The text you input overlimit" + ' %s'%(len(location)-100) +" characters"))
        return location
    def clean_store_story(self):
        store_story=self.cleaned_data.get('store_story')
        if len(store_story) > 1000:
            raise forms.ValidationError(_(u"The text you input overlimit" + ' %s'%(len(store_story)-1000) +" characters"))
        return store_story
    def clean_telephone(self):
        telephone=self.cleaned_data.get('telephone')
        phone_area=self.cleaned_data.get('phone_area')
        country = self.cleaned_data.get('country')
        if country == '1':
            if telephone and not phone_area:
               raise forms.ValidationError(_(u"Please choose your phone area code"))
            if re.search('[a-zA-Z]',telephone):
                raise forms.ValidationError(_(u'Telephone must numeric'))
            else:
                return telephone
        else:
            if not telephone:
                raise forms.ValidationError(_(u"Please type your telephone number"))
            else:
                return telephone
    def clean_handphone(self):
        handphone=self.cleaned_data.get('handphone')
        if re.search('[a-zA-Z]',handphone):
            raise forms.ValidationError(_(u'Handphone must numeric'))
        else:
            return handphone
    def clean_fax(self):
        fax=self.cleaned_data.get('fax')
        fax_code=self.cleaned_data.get('fax_code')
        country = self.cleaned_data.get('country')
        if country=="1":
            if fax and not fax_code:
               raise forms.ValidationError(_(u"Please choose your fax area code"))
            if re.search('[a-zA-Z]',fax):
                raise forms.ValidationError(_(u'Facimile must numeric'))
            else:
                return fax
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        instance_picture = self.instance.picture
        if instance_picture!=picture:
            if picture._size>settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(picture._size)))
        return picture
    def clean_promotion_text(self):
        promotion_text=self.cleaned_data.get('promotion_text')
        if len(promotion_text) > 1000:
            raise forms.ValidationError(_(u"The text you input overlimit" + ' %s'%(len(promotion_text)-1000) +" characters"))
        return promotion_text
    
    

class AddStoreForm(StoreForm):
    location = forms.CharField(help_text=_(u'Max length is 100 character'),widget=forms.Textarea(attrs={'maxlength':100,'rows':5}))
    class Meta(StoreForm.Meta):
        pass
#    def save(self,commit=True):
#        new_store=super(AddStoreForm,self).save(commit=commit)
#        new_line=Line(store=new_store,line=new_store.name+"'s Line")
#        new_line.save()
        

class EditStoreForm(StoreForm):
    
    class Meta(StoreForm.Meta):
        fields=[
        'name',
        'location',
        'country',
        'province',
        'post_code',
        'phone_area',
        'telephone',
        'handphone',
        'fax_code',
        'fax',
        'company_website',
        'store_story',
        'picture',
        'promotion_text',
#          'last_updated',
        ]
    def __init__(self, *args, **kwargs):
      super(StoreForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields

    def clean_name(self):
      user = self.instance.user
      name = self.cleaned_data.get('name')
      exist_store = Store.objects.filter(name=name,deleted=False).exclude(user=user)
      if exist_store:
          raise forms.ValidationError(_(u"Store name had been used by someone else."))
      return name


class ItemForm(forms.ModelForm):
    description = forms.CharField(help_text=_(u'Max Length 800 character'),widget=forms.Textarea(attrs={'maxlength':800,'rows':5}))
    currency = forms.ModelChoiceField(Currency.objects.order_by('title'),required=True)
    price = forms.IntegerField(min_value=0,max_value=999999999,widget=forms.TextInput(attrs={'maxlength':9}),help_text=_(u'if price is 0 then the price is based on request'))
    class Meta:
        model = Item
        fields=[
            'item_code',
            'item',
            'description',
            'gender',
            'colour',
            'size',
            'currency',
            'price',
            'availability',
            'picture1',
            'picture2',
        ]
    def __init__(self, *args, **kwargs):
      super(ItemForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields
    def clean_description(self):
        description=self.cleaned_data.get('description')
        if len(description) > 800:
            raise forms.ValidationError(_(u'The maximum length of description must 800 character'))
        return description
    def clean_colour(self):
        colour=self.cleaned_data.get('colour')
        if re.search('[0-9]',colour):
            raise forms.ValidationError(_(u'Colour must Alphabet'))
        return colour
    def clean_price(self):
        price = self.cleaned_data.get('price')
        currency = self.cleaned_data.get('currency')
        if not currency :
              raise forms.ValidationError(_(u'Please choose currency.'))
        return price
    def clean_picture1(self):
        picture1 = self.cleaned_data.get('picture1')
        instance_pic = self.instance.picture1
        if picture1:
          if instance_pic!=picture1:
            if picture1._size>settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(picture1._size)))
        else:
            raise forms.ValidationError(_('This field is required'))
        return picture1
    def clean_picture2(self):
        picture2 = self.cleaned_data.get('picture2')
        instance_pic = self.instance.picture2
        if picture2:
           if instance_pic!=picture2:
            if picture2._size>settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(picture2._size)))
        return picture2
        
class EditItemForm(ItemForm):
    class Meta(ItemForm.Meta):
        pass

    
class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields=[
        'line',
        'category',
        ]

class EditLineForm(LineForm):
    class Meta(LineForm.Meta):
        fields=[
        'line',
        ]
    def __init__(self, *args, **kwargs):
      super(LineForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields
      
class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'maxlength':1000}))
    class Meta:
        model = Comment
        fields=[
        'comment',
        ]
    def __init__(self, *args, **kwargs):
      super(CommentForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields
    def clean_comment(self):
        comment=self.cleaned_data.get('comment')
        if len(comment) > 1000:
            raise forms.ValidationError(_(u'Maximum length is 1000 character.'))
        return comment
    
class SearchStoreForm(forms.Form):
    keyword = forms.CharField(label=_(u'Search Stores'))
    category = forms.ModelChoiceField(LineCategory.objects.all(),empty_label=_('All'))
    line = ModelFkChoiceField(Line.objects.all(),fk='category_id',empty_label=_('All'))
    class Meta:
        fields=[
            'keyword',
            'category',
            'line',
            ]

    def __init__(self, *args, **kwargs):
        super(SearchStoreForm, self).__init__(*args, **kwargs)
#        temp_line = []
#        temp_line_id=[]
#        lines = Line.objects.filter(store__deleted=False)
#        for line in lines:
#            if temp_line:
#                if not line.line in temp_line:
#                    temp_line.append(line.line)
#                    temp_line_id.append(line.id)
#            else:
#                temp_line.append(line.line)
#                temp_line_id.append(line.id)
#        lines=lines.filter(id__in=temp_line_id)
#        self.fields['line'] = ModelFkChoiceField(lines,fk='category_id')
        self.fields.keyOrder = self.Meta.fields

class SearchItemForm(forms.Form):
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
    (UNISEX,'UNISEX'),
    (MALE,'MALE'),
    (FEMALE,'FEMALE'),
    )
    keywords = forms.CharField(label=_(u'Search Fashion'))
    category = forms.ModelChoiceField(LineCategory.objects.order_by('name'),empty_label=_('All'))
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    availability = forms.ChoiceField(choices=AVAILABILITY_CHOICE)
    class Meta:
        fields=[
            'keywords',
            'category',
            'gender',
            'availability',
            ]

    def __init__(self, *args, **kwargs):
        super(SearchItemForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = self.Meta.fields
        
class VoucherForm(forms.Form):
    user_email = forms.EmailField(label=_('Send more info into my email'))
    class Meta:
        fields=['user_email',]
    def __init__(self, *args, **kwargs):
      super(VoucherForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields
