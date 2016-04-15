from django.shortcuts import render_to_response
from django import forms
from django.template.context import RequestContext
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from widgets import NamelessRadioInput
from fields import TempImageField

__all__=('SearchForm','MultiImageForms')

def create_image_form(model0,image_field0,fields0):
    image_field = image_field0
    class ImageForm(forms.ModelForm):
      make_default=forms.CharField(required=False)
      delete=forms.BooleanField(required=False)
      delete2=forms.BooleanField(required=False)

      class Meta:
        model=model0
        fields=fields0
      def __init__(self, *args, **kwargs):
            super(ImageForm, self).__init__(*args, **kwargs)
            self.fields[image_field]=TempImageField()
            self.fields.keyOrder = self.Meta.fields
    return ImageForm

class MultiImageForms(object):
    one_saved_or_deleted=False
    size = getattr(settings,'MAX_UPLOAD_SIZE',1000000)
    need_to_set_default_image=False

    def __unicode__(self):
        return 'MultiImagesForm'

    def __init__(self,image,image_owner=None,num_uploads=1,image_limit=1,data=None,files=None):
        self.image_limit=image_limit
        self.num_uploads=num_uploads
        self.image_field = 'image'

        self.image_owner_field=image[1]
        self.image_owner_image_field=None
        self.image_owner = None

        if image_owner: 
            self.image_owner=image_owner[0]
            self.image_owner_image_field=image_owner[1]

            filter_dict={self.image_owner_field:self.image_owner}
            self.image_list=image[0].objects.filter(**filter_dict)
        else:
            self.image_list=[]

        self.AddImageForm=create_image_form(image[0],self.image_field,[self.image_field,])
        self.EditImageForm=create_image_form(image[0],self.image_field,['make_default','delete'])

        self.data=data
        self.files=files
        
        self.num_images=len(self.image_list)

        if self.num_images <= 0:
          self.need_to_set_default_image=True

    def is_valid(self):
        return self.one_saved_or_deleted

    def is_saved(self):
        return self.one_saved_or_deleted

    def __iter__(self):
        num_uploads_count=0
        for i in xrange(0,self.image_limit): 
            try:
                #EDIT EXISTING IMAGE FORM
                if self.data or self.files:
                    form=self.EditImageForm(prefix=i,instance=self.image_list[i],data=self.data,files=self.files)
                    form.is_valid()
                    #raise Exception(self.image_list[i])
                else:
                    form=self.EditImageForm(prefix=i,instance=self.image_list[i])
                form.fields['make_default']=forms.CharField(required=False,label=_(u"Make Default"),widget=NamelessRadioInput(attrs={'name':'make_default'}),initial=form.instance.pk)
                if getattr(self.image_owner,'%s_id' % self.image_owner_image_field) == form.instance.id:
                    form.fields['make_default'].widget=NamelessRadioInput(attrs={'name':'make_default','checked':''})
            except IndexError:
                #ADD NEW IMAGE FORM
                if self.data or self.files:
                    form=self.AddImageForm(prefix=i,data=self.data,files=self.files)
                    form.is_valid()
                else:
                    form=self.AddImageForm(prefix=i)
                #raise Exception(form)
                if num_uploads_count < self.num_uploads:
                    num_uploads_count+=1
                else:
                    form.fields[self.image_field].widget.attrs={'disabled':''}

            yield form #append all looped forms to list

    def set_image_owner_image(self,image):
        setattr(self.image_owner,self.image_owner_image_field,image)

    def get_image_owner_image(self):
        return getattr(self.image_owner,self.image_owner_image_field)

    def save(self):
        if self.data.get('make_default'):
            #'make default' checkbox is not part of modelform,
            #so catch this POST item and save it to product.default_image
            self.set_image_owner_image(self.image_list.get(id=int(self.data.get('make_default'))))
            self.image_owner.save()
            self.need_to_set_default_image=False

        """
        if not self.get_image_owner_image() and self.num_images > 0:
            self.set_image_owner_image(self.image_list[0])
            self.image_owner.save()
            self.need_to_set_default_image=False
        """
            
        for i in xrange(0,self.image_limit): 
            try:
                #EDIT EXISTING IMAGE FORM
                form=self.EditImageForm(prefix=i,instance=self.image_list[i],data=self.data,files=self.files)
            except IndexError:
                #ADD NEW IMAGE FORM
                form=self.AddImageForm(prefix=i,data=self.data,files=self.files)

            if form.is_valid():
              if form.cleaned_data.get('delete'):
                # DELETING image
                if self.get_image_owner_image() == form.instance:
                  #product has the deletion image as default image, 
                  #so null it first
                  #!OR ELSE PRODUCT GETS DELETED!
                  self.set_image_owner_image(None)
                  self.image_owner.save()
                  self.need_to_set_default_image=True 

                form.instance.delete()           
                self.one_saved_or_deleted=True
              else:
                # ADDING or CHANGING image
                if self.data.get('%s_tmp' % self.image_field) or self.data.get('%s-%s_tmp' % (i,self.image_field)) or self.files:
                    #new image upload
                    new_image=form.save(commit=False)
                    setattr(new_image,self.image_owner_field,self.image_owner)
                    new_image.save()

                if self.need_to_set_default_image : 
                  #there are currently no existing image, 
                  #so set this new image as default
                  try:
                      self.set_image_owner_image(new_image)
                  except NameError:
                      self.set_image_owner_image(form.instance)
                  self.image_owner.save()
                  self.need_to_set_default_image=False
  
                self.one_saved_or_deleted=True

class SearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
      super(SearchForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields
  
    def search(self,queryset=None):
        for field_name in self.fields:
            #all fields are set to be NOT required
            self.fields[field_name].required=False

        if not queryset:
            queryset = self.Meta.model.objects.all()

        if not self.is_valid():
            return queryset 

        #if GET id, return the object immediately, no need to do a complex filter
        if self.cleaned_data.get('id'):
            # doing filter instead of get, because the template is alreadyset to loop, so you need a list not just a single item
            return queryset.filter(pk=self.cleaned_data.get('id'))

        kwargs = dict()
        exclude_kwargs = dict()
        try:
            form_fields=self.Meta.fields
        except AttributeError:
          raise "Meta must have 'fields' attribute"
        
        for field in self.Meta.model._meta.fields: 
          if self.cleaned_data.get(field.name):
            if str(self.cleaned_data.get(field.name))[0]  == '!':
                exclude_kwargs[field.name]=self.cleaned_data.get(field.name)
            else:
                kwargs[field.name]=self.cleaned_data.get(field.name)
        
        try:
            for arg in self.Meta.filter_args.items():
              if self.cleaned_data.get(arg[0]):
                if str(self.cleaned_data.get(arg[0]))[0]  == '!':
                    exclude_kwargs[arg[1]]=self.cleaned_data.get(arg[0])[1:]
                else:
                    #eg. replacing key brand with brand__icontains
                    if arg[0] in kwargs:
                        del kwargs[arg[0]]
                    kwargs[arg[1]]=self.cleaned_data.get(arg[0])
            """
            for field in self.cleaned_data.items():
              if self.Meta.filter_args.has_key(str(field[0])) and field[1]:
                #this filter argument is allowed, and has a request value
                if self.Meta.filter_args.get(str(field[0])):
                    if field[1][0] == '!':
                      #first character in GET value is !, meaning NOT
                      exclude_kwargs[str(self.Meta.filter_args[field[0]])] = field[1][1:]
                    else:
                      #use correct query specified in filter args
                      kwargs[str(self.Meta.filter_args[field[0]])] = field[1]
                else:
                  kwargs[str(field[0])] = field[1]
            """

            """
            eg.
            kwargs={
                'model__brand':1,
                'model':2
            }

            filter_args={
              'brand':'model__brand',
              'price_min':'price__gte',
              'price_max':'price__lte',
              'public_or_showroom':'sub_user__sub_group__slug'
            }

            model_fk_list=(
              {'model':'model','fk':'brand'},
            )
            kwargs = 
            """

            for model_fk in self.Meta.model_fk_list: 
              #eg. model has foreign key to brand, if filter for model exists, you don't need to filter for brand
              if model_fk['model'] in kwargs and model_fk['fk'] in kwargs:
                del kwargs[self.Meta.filter_args[model_fk['fk']]]

        except AttributeError:
            pass

        if 'sort_by' in self.Meta.fields and self.cleaned_data.get('sort_by'):
            sort_by=self.cleaned_data.get('sort_by')
            queryset=queryset.order_by(sort_by)
        else:
            try: 
                sort_by=self.Meta.default_sort_by
                queryset=queryset.order_by(sort_by)
            except AttributeError:
                pass

        return queryset.filter(**kwargs).exclude(**exclude_kwargs)
