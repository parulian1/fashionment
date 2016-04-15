#imports for modelfkchoicefield
from django import forms
from django.utils.encoding import smart_unicode
from django.forms.fields import ChoiceField,Field
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from widgets import SelectFk
import librecaptcha
from django.conf import settings
#imports for indphonefield
from django.forms.fields import RegexField
from django.utils.translation import ugettext_lazy as _
import re
from django.forms.util import ErrorList, ValidationError
#phone_num_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
#phone_num_re = re.compile(r'^(\d{3,4})[- ]?\d+$')
phone_num_re = re.compile(r'^[\d]+$')

class IndoPhoneField(RegexField):
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

class ModelFkChoiceField(ModelChoiceField):
    widget=SelectFk
    def __init__(self, queryset, empty_label=u"---------", cache_choices=False,
                 required=True, widget=None, label=None, initial=None,
                 help_text=None, to_field_name=None,fk=None, *args, **kwargs):
        self.empty_label = empty_label
        self.cache_choices = cache_choices
        self.fk=fk

        # Call Field instead of ChoiceField __init__() because we don't need
        # ChoiceField.__init__().
        Field.__init__(self, required, widget, label, initial, help_text,
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
        return ModelChoiceIterator(self)

    choices = property(_get_choices, ChoiceField._set_choices)

class ModelChoiceIterator(object):
    def __init__(self, field):
        self.field = field
        self.queryset = field.queryset

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
            #TODO this if statement seems to be of no use
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

class ReCaptcha(forms.Widget):
    input_type = None # Subclasses must define this.

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        html = u"<script>var RecaptchaOptions = {theme : '%s'};</script>" % (
            final_attrs.get('theme', 'white'))
        html += librecaptcha.displayhtml(public_key=settings.RECAPTCHA_PUBLIC,ajax_js='%sjs/recaptcha_ajax.js' % settings.MEDIA_URL)
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        return {
            'recaptcha_challenge_field': data.get('recaptcha_challenge_field', None),
            'recaptcha_response_field': data.get('recaptcha_response_field', None),
        }

# hack: Inherit from FileField so a hack in Django passes us the
# initial value for our field, which should be set to the IP
class ReCaptchaField(forms.FileField):
    widget = ReCaptcha
    default_error_messages = {
        'invalid-site-public-key': u"Invalid public key",
        'invalid-site-private-key': u"Invalid private key",
        'invalid-request-cookie': u"Invalid cookie",
        'incorrect-captcha-sol': u"Invalid entry, please try again.",
        'verify-params-incorrect': u"The parameters to verify were incorrect, make sure you are passing all the required parameters.",
        'invalid-referrer': u"Invalid referrer domain",
        'recaptcha-not-reachable': u"Could not contact reCAPTCHA server",
    }

    def clean(self, data, initial):
        if initial is None or initial == '':
            raise Exception("ReCaptchaField requires the client's IP be set to the initial value")
        ip = initial
        resp = librecaptcha.submit(data.get("recaptcha_challenge_field", None),
                              data.get("recaptcha_response_field", None),
                              settings.RECAPTCHA_PRIVATE, ip)
        if not resp.is_valid:
            raise forms.ValidationError(self.default_error_messages.get(
                    resp.error_code, "Unknown error: %s" % (resp.error_code)))


