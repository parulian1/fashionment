from django import forms

""" imports for modelfkchoicefield """
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from widgets import SelectFk,SelectMultipleFk
from django.forms.models import ModelChoiceIterator

""" for indphonefield """
from django.utils.translation import ugettext_lazy as _
import re
from django.forms.util import ErrorList, ValidationError
#phone_num_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
#phone_num_re = re.compile(r'^(\d{3,4})[- ]?\d+$')

""" for recaptcha field """
from extra import librecaptcha
from django.conf import settings
from django.utils.safestring import mark_safe

""" for cachedModelChoiceField """
from django.core.cache import cache 
from django.db.models.query import QuerySet

""" for serilizedWidget"""
from django.utils import simplejson

""" for tempfilefield/widget """
import os
from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import SimpleUploadedFile

__all__=(
    'IndoPhoneField',
    'ModelFkChoiceField',
    'ModelFkMultipleChoiceField',
    'CachedModelChoiceField',
    'ReCaptchaField',
    'SwfField',
    'TempImageField',
)

phone_num_re = re.compile(r'^[\d]+$')

class IndoPhoneField(forms.RegexField):
    default_error_messages = {
        'invalid': _(u'Enter numbers only.'),
        'not_exist':_(u'The area code does not exist.')
    }
    def __init__(self, *args, **kwargs):
        super(IndoPhoneField, self).__init__(phone_num_re, *args, **kwargs)

    def clean(self, value):
        """
        Validates that the input matches the regular expression. Returns a
        Unicode object.
        """
        value = super(IndoPhoneField, self).clean(value)
        if value == u'':
            return value

        phone_number=self.regex.search(value)
        if not phone_number:
            #regex fail, invalid phone number
            raise ValidationError(self.error_messages['invalid'])
        
        return value

def model_choice_field_clean(obj,value):
    #this clean makes sure value ALWAYS be INT
    try:
        value == '' or value is None or type(int(value)) is int
    except ValueError:
        #catches if int(value) fails to return an integer
        raise ValidationError(obj.error_messages['invalid_choice'])    
    return forms.ModelChoiceField.clean(obj,value)

class ModelFkChoiceField(forms.ModelChoiceField):
    widget=SelectFk
    def __init__(self, queryset, empty_label=u"--------", cache_choices=False,
                 required=True, widget=None, label=None, initial=None,
                 help_text=None, to_field_name=None,fk=None, *args, **kwargs):
        self.empty_label = empty_label
        self.cache_choices = cache_choices
        self.fk=fk

        # Call Field instead of ChoiceField __init__() because we don't need
        # ChoiceField.__init__().
        forms.Field.__init__(self, required, widget, label, initial, help_text,
                       *args, **kwargs)
        self.queryset = queryset
        self.choice_cache = None
        self.to_field_name = to_field_name
        
    def _get_choices(self):
        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices

        #return(('boo',(('booo','booo'),)),('boo','boo'),('boo','boo'))
        return ModelFkChoiceIterator(self)
    
    def clean(self, value):
        return model_choice_field_clean(self,value)

    choices = property(_get_choices, forms.ChoiceField._set_choices)

class ModelFkChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label,u"")
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset.all()
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset.all():
                yield self.choice(obj)

    def choice(self, obj):
        if self.field.to_field_name:
             #FIXME: The try..except shouldn't be necessary here. But this is
             # going in just before 1.0, so I want to be careful. Will check it
             # out later.
            try:
                key = getattr(obj, self.field.to_field_name).pk
            except AttributeError:
                key = getattr(obj, self.field.to_field_name)
        else:
            key = obj.pk
            fkey=''
            if self.field.fk:
              try:
                fkey = getattr(obj, self.field.fk)
              except AttributeError:
                pass

        #TODO learn about generators
        #return (obj.name,[(model.id,model.name) for model in obj.model_set.all()])
        #return (obj.brand_id, ((key,self.field.label_from_instance(obj)),))
        return (key, self.field.label_from_instance(obj),fkey)

class ModelFkMultipleChoiceField(ModelFkChoiceField):
    widget=SelectMultipleFk
    hidden_widget = forms.MultipleHiddenInput                                        
    default_error_messages = {                                                 
        'list': _(u'Enter a list of values.'),
        'invalid_choice': _(u'Select a valid choice. %s is not one of the'     
                            u' available choices.'),                           
    } 
    
    def __init__(self, queryset, cache_choices=False, required=True,
                 widget=None, label=None, initial=None,                        
                 help_text=None, *args, **kwargs):                             
        super(ModelFkMultipleChoiceField, self).__init__(queryset, None,
            cache_choices, required, widget, label, initial, help_text,        
            *args, **kwargs)                                                   
                                                                               
    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        elif not self.required and not value:                                  
            return []
        if not isinstance(value, (list, tuple)):                               
            raise ValidationError(self.error_messages['list'])
        final_values = []
        for val in value:
            try:       
                obj = self.queryset.get(pk=val)                                
            except self.queryset.model.DoesNotExist:                           
                raise ValidationError(self.error_messages['invalid_choice'] % val)              
            else:                                                              
                final_values.append(obj)                                       
        return final_values

class CachedModelChoiceField(forms.ModelChoiceField):
    def __init__(self, queryset, cache_key, duration=60, empty_label=u"---------", cache_choices=False,
                 required=True, widget=None, label=None, initial=None,
                 help_text=None, to_field_name=None, *args, **kwargs):
        self.empty_label = empty_label
        self.cache_choices = cache_choices

        # Call Field instead of ChoiceField __init__() because we don't need
        # ChoiceField.__init__().
        forms.Field.__init__(self, required, widget, label, initial, help_text,
                       *args, **kwargs)

        cached = cache.get(cache_key)
        if cached is QuerySet:
          self.queryset = cached
        else:
          self.queryset = queryset
          cache.set(cache_key, queryset, duration)

        self.choice_cache = None
        self.to_field_name = to_field_name

    def _get_choices(self):
        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices

        # Otherwise, execute the QuerySet in self.queryset to determine the
        # choices dynamically. Return a fresh QuerySetIterator that has not been
        # consumed. Note that we're instantiating a new QuerySetIterator *each*
        # time _get_choices() is called (and, thus, each time self.choices is
        # accessed) so that we can ensure the QuerySet has not been consumed. This
        # construct might look complicated but it allows for lazy evaluation of
        # the queryset.
        return CachedModelChoiceIterator(self)
    
    def clean(self, value):
        return model_choice_field_clean(self,value)

    choices = property(_get_choices, forms.ChoiceField._set_choices)

class CachedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset.all()
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset: #Change to ONLY this line. Removed .all()
                yield self.choice(obj)

class ReCaptchaWidget(forms.Widget):
    input_type = None # Subclasses must define this.

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        html = u"<script>var RecaptchaOptions = {theme : '%s'};</script>" % (
            final_attrs.get('theme', 'white'))
        html += librecaptcha.displayhtml(public_key=getattr(settings,'RECAPTCHA_PUBLIC',''),ajax_js='%sjs/recaptcha_ajax.js' % settings.MEDIA_URL,name=name)
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        return {
            'recaptcha_challenge_field': data.get('recaptcha_challenge_field', None),
            'recaptcha_response_field': data.get(name, None),
            'recaptcha_ip': data.get('recaptcha_ip_field',None)
        }

# hack: Inherit from FileField so a hack in Django passes us the
# initial value for our field, which should be set to the IP
from extra import registration
class ReCaptchaField(forms.FileField):
    widget = ReCaptchaWidget
    default_error_messages = {
        'invalid-site-public-key': u"Invalid public key",
        'invalid-site-private-key': u"Invalid private key",
        'invalid-request-cookie': u"Invalid cookie",
        'incorrect-captcha-sol': _(u"Invalid entry, please try again."),
        'verify-params-incorrect': u"The parameters to verify were incorrect, make sure you are passing all the required parameters.",
        'invalid-referrer': u"Invalid referrer domain",
        'recaptcha-not-reachable': u"Could not contact reCAPTCHA server",
    }

    def clean(self, data, initial):
        if not getattr(settings,'RECAPTCHA_PRIVATE',False):
            #RECAPTCHA_PRIVATE does not exist in settings
            return data

        if data.get('recaptcha_ip',False):
            ip = data['recaptcha_ip']
        elif initial:
            ip = initial
        else:
            raise Exception("ReCaptchaField requires the client's IP be set to the initial value OR add ReCaptchaMiddleware to settings.py")
        resp = librecaptcha.submit(data.get("recaptcha_challenge_field", None),
                              data.get("recaptcha_response_field", None),
                              getattr(settings,'RECAPTCHA_PRIVATE',''), 
                              ip)
        if not resp.is_valid:
            raise forms.ValidationError(self.default_error_messages.get(
                    resp.error_code, "Unknown error: %s" % (resp.error_code)))

class SwfField(forms.FileField):
  def clean(self, data, initial=None):
    super(SwfField, self).clean(data,initial)

    file_extension = data.name[-4:]
    if file_extension != '.swf':
      raise forms.ValidationError(_(u'Upload a proper SWF file.'))

    return data

    """
    super(FileField, self).clean(initial or data)
    if not self.required and data in EMPTY_VALUES:
        return None
    elif not data and initial:
        return initial

    # UploadedFile objects should have name and size attributes.
    try:
        file_name = data.name
        file_size = data.size
    except AttributeError:
        raise ValidationError(self.error_messages['invalid'])

    if not file_name:
        raise ValidationError(self.error_messages['invalid'])
    if not file_size:
        raise ValidationError(self.error_messages['empty'])

    return data
    """
from django import forms 
from django.conf import settings
from django.forms.fields import EMPTY_VALUES
from django.utils.translation import ugettext as _, ungettext

from extra.BeautifulSoup import BeautifulSoup, Comment

class CleanCharField(forms.CharField):
	valid_tags= getattr(settings,'VALID_TAGS','p i strong b u a h1 h2 h3 pre br img ul li').split()
	valid_attrs= getattr(settings,'VALID_ATTRS','href src').split()

	def clean(self, value):
		"""
			Checks that the given string has no profanities in it. This does a simple
			check for whether each profanity exists within the string, so 'fuck' will
			catch 'motherfucker' as well. Raises a ValidationError such as:
			Watch your mouth! The words "f--k" and "s--t" are not allowed here.
		"""
		value= value.lower() # normalize
		words_seen= [w for w in settings.PROFANITIES_LIST if w in value]
		if words_seen:
			from django.utils.text import get_text_list
			plural= len(words_seen)
			raise forms.ValidationError, ungettext("Watch your mouth! The word %s is not allowed here.",
				"Watch your mouth! The words %s are not allowed here.", plural) % \
				get_text_list(['"%s%s%s"' % (i[0], '-'*(len(i)-2), i[-1]) for i in words_seen], _('and'))
		"""
			Cleans non-allowed HTML from the input
		"""
		value= super(CleanCharField, self).clean(value)
		soup= BeautifulSoup(value)
		for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
			comment.extract()
		for tag in soup.findAll(True):
			if tag.name not in self.valid_tags:
				tag.hidden= True
				tag.attrs= [(attr, val) for attr, val in tag.attrs if attr in self.valid_attrs]
		return soup.renderContents().decode('utf8')


class SerializedWidget(forms.MultiWidget):
    def __init__(self,attrs=None):
        super(SerializedWidget, self).__init__(self.widgets, attrs=attrs)

    def decompress(self, value):
        #raise Exception(type(value))
        if value:
            data_dict = simplejson.loads(value)
            data_list=[]
            for field in self.fields:
                if data_dict.get(field.name):
                    data_list.append(data_dict[field.name])
            return data_list

        return [None, None]

    def format_output(self, rendered_widgets):
        html=''
        i=0
        for widget in rendered_widgets:
            if self.fields[i].label:
                label = self.fields[i].label
            else:
                label = self.fields[i].name
            html='%s%s%s' % (html,label,widget)
            i+=1
        return html

class SerializedField(forms.MultiValueField):
    widget = SerializedWidget
    def __init__(self, fields, *args, **kwargs):
        self.widget.fields=[]
        for name,field in fields.items():
            field.name=name
            self.widget.fields.append(field)
        self.widget.widgets=[field.widget for field in self.widget.fields]
        super(SerializedField, self).__init__(self.widget.fields, *args, **kwargs)
    def compress(self, data_list):
        dict={}
        i=0
        if data_list:
            for field in self.fields:
                dict[field.name]=data_list[i]
                i+=1
        return simplejson.dumps(dict)

class TempImageWidget(forms.FileInput):
    def render(self,name,value,attrs=None):
        return mark_safe('''<img src="%s" /> 
            <input type="hidden" name="%s_tmp" value="%s" />
            <input type="hidden" name="%s_tmp_name" value="%s" />
            %s''' % (
                self.tmp_file_url,
                name,self.tmp_file_path,
                name,self.tmp_file_name,
                super(TempImageWidget,self).render(name=name,value=value,attrs=attrs)
            ))
    def value_from_datadict(self, data, files, name):
        return {
            'file': files.get(name, None),
            'tmp_file_path': data.get(name+'_tmp', None),
            'tmp_file_name': data.get(name+'_tmp_name',None)
        }
    
class TempImageField(forms.ImageField):
    widget = TempImageWidget
    """
        CHECKING FOR PROPERLY CONFIGURED SETTINGS
    """
    if hasattr(settings,'FILE_UPLOAD_HANDLERS'):
        for line in settings.FILE_UPLOAD_HANDLERS:
            if 'MemoryFileUploadHandler' == line.split('.')[-1]:
                raise ImproperlyConfigured('TempImageField cannot work if MemoryFileUploadHandler is in FILE_UPLOAD_HANDLERS. RECOMMEND using extra.core.files.uploadhandler.TemporaryFileUploadHandler in FILE_UPLOAD HANDLERS, so that temporary directory will be auto created.')
    else:
        raise ImproperlyConfigured('FILE_UPLOAD_HANDLERS must be in settings which does not contain MemoryFileUploadHandler, RECOMMEND using extra.core.files.uploadhandler.TemporaryFileUploadHandler, so that temporary directory will be auto created.')
    if not hasattr(settings,'FILE_UPLOAD_TEMP_URL_DIR'):
        raise ImproperlyConfigured('FILE_UPLOAD_TEMP_URL_DIR must be in settings.py which also needs FILE_UPLOAD_TEMP_DIR to match') 

    def __init__(self,*args,**kwargs):
        super(TempImageField,self).__init__(*args,**kwargs)
        self.widget.tmp_file_path=''
        self.widget.tmp_file_url=''
        self.widget.tmp_file_name=''
    def clean(self,data,initial=None):
        if self.required and not (data.get('file') or (data.get('tmp_file_path') and data.get('tmp_file_name'))):
            raise ValidationError(self.error_messages['required'])
        if data['file']:
            file = data['file']
            super(TempImageField,self).__init__(file,initial)
            tmp_file_path = file.temporary_file_path()
            tmp_file_name = os.path.split(tmp_file_path)[-1]
            tmp_file_url = os.path.join(settings.FILE_UPLOAD_TEMP_URL_DIR, tmp_file_name)
            self.widget.tmp_file_path = tmp_file_path 
            self.widget.tmp_file_url = tmp_file_url 
            self.widget.tmp_file_name = file.name

        elif data['tmp_file_path'] and os.path.exists(data['tmp_file_path']):
            file = open(data['tmp_file_path'],'rb')
            file = SimpleUploadedFile(data['tmp_file_name'],file.read())
        else:
            raise ValidationError('Sorry you took too long to submit. Please upload picture again.')

        return file
