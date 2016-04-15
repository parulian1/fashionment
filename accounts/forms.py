from django import forms
import re,sha,random
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
from django.forms.widgets import DateTimeInput
from accounts.models import User, CountryAreaCode,ProvinceAreaCode,PhoneAreaCode
from extra.fields import ModelFkChoiceField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from extra.forms.fields import ReCaptchaField

class MyDateInput(DateTimeInput):
  format = '%d/%m/%Y'
  
SHA1_RE = re.compile('^[a-f0-9]{40}$')

class UserForm(forms.ModelForm):
    email=forms.EmailField()
    username=forms.CharField(label=_(u'Username'))
    password=forms.CharField(label=_(u'Password'),widget=forms.PasswordInput(),help_text=_(u'Minimum of 6 characters, must have a number and an alphabet'))
    personal_website = forms.URLField(required=False,help_text='http://example.com/')
    confirm_password=forms.CharField(label=_(u'Confirm Password'),widget=forms.PasswordInput())
    country = forms.ModelChoiceField(CountryAreaCode.objects.order_by('country_name'))
    province = ModelFkChoiceField(ProvinceAreaCode.objects.order_by('province_name'),fk='country_id',required=False)
    phone_area_code = ModelFkChoiceField(PhoneAreaCode.objects.order_by('code'),fk='prov_id',required=False)
    fax_area_code = ModelFkChoiceField(PhoneAreaCode.objects.order_by('code'),fk='prov_id',required=False)
    street_address=forms.CharField(help_text=_(u'Max length is 1000 character'),widget=forms.Textarea(attrs={'maxlength':1000,'rows':5}))
    about_me=forms.CharField(help_text=_(u'Max length is 1000 character'),widget=forms.Textarea(attrs={'maxlength':1000,'rows':5}))
    checkbox = forms.BooleanField(help_text=_(u"I Agree To Fashionment's Terms And Agreements, And Certify That I Am 17 Years Of Age Or Over. "))
    account_type = forms.ChoiceField(widget=forms.widgets.RadioSelect,choices=User.ACCOUNT_TYPE,label=_(u'Account type'))
    post_code = forms.IntegerField(min_value=0,max_value=999999,widget=forms.TextInput(attrs={'maxlength':6}))
    date_of_birth=forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=MyDateInput(),
        help_text='eg.31/12/2009',
        )
    recaptcha=ReCaptchaField()
    class Meta:
        model=User
        fields=[
          'username',
          'first_name',
          'last_name',
          'sex',
          'interest',
          'email',
          'password',
          'confirm_password',
          'country',
          'province',
          'phone_area_code',
          'telephone',
          'handphone',
          'fax_area_code',
          'fax',
          'street_address',
          'post_code',
          'date_of_birth',
          'personal_website',
          'about_me',
          'picture',
          'account_type',
          'checkbox',
          'recaptcha',
            ]
    def __init__(self, *args, **kwargs):
      super(UserForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields
      
    def clean_province(self):
        country = self.cleaned_data.get('country')
        province = self.cleaned_data.get('province')
        if country=="1":
            if not province:
                raise forms.ValidationError(_(u"Please choose your province"))
            else:
                return province
    def clean_street_address(self):
        street_address=self.cleaned_data.get('street_address')
        if len(street_address) > 1000:
            raise forms.ValidationError(_(u'The maximum length of Street Address must 1000 character'))
        return street_address    
    def clean_about_me(self):
        about_me=self.cleaned_data.get('about_me')
        if len(about_me) > 1000:
            raise forms.ValidationError(_(u'The maximum length of About me  must 1000 character'))
        return about_me
    def clean_telephone(self):
        telephone=self.cleaned_data.get('telephone')
        phone_area_code=self.cleaned_data.get('phone_area_code')
        country = self.cleaned_data.get('country')
        if country == '1':
            if telephone and not phone_area_code:
               raise forms.ValidationError(_(u"Please choose your phone area code"))
            if re.search('[a-zA-Z]',telephone):
                raise forms.ValidationError(_(u'Telephone must numeric'))
            else:
                return telephone
        else:
            if not telephone:
                raise forms.ValidationError(_(u"Please add your telephone number"))
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
        fax_area_code=self.cleaned_data.get('fax_area_code')
        country = self.cleaned_data.get('country')
        if country =="1":
            if fax and not fax_area_code:
               raise forms.ValidationError(_(u"Please choose your fax area code"))
            if re.search('[a-zA-Z]',fax):
                raise forms.ValidationError(_(u'Facimile must numeric'))
            else:
                return fax

    def clean_password(self):
        password=self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError(_(u'Password must be 6 characters or more.'))
        elif not re.search('[0-9]',password):
            raise forms.ValidationError(_(u'Please have at least 1 number in your password'))
        elif not re.search('[a-zA-Z]',password):
            raise forms.ValidationError(_(u'Please have at least 1 alphabet in your password'))
        return password

    def clean_confirm_password(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            raise forms.ValidationError(_(u'Passwords Do Not Match!'))

        return self.cleaned_data.get('confirm_password')
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        instance_picture = self.instance.picture

        if picture:
          if instance_picture != picture:
            if picture._size>settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(picture._size)))
        return picture

class ResetPasswordConfirmForm(forms.Form):
    new_password1=forms.CharField(label=_(u'Pass1word'),widget=forms.PasswordInput(),help_text=_(u'Minimum of 6 characters, must have a number and an alphabet'))
    new_password2=forms.CharField(label=_(u'Confirm Password'),widget=forms.PasswordInput())
    class Meta:
        model = User
        fields=[
          'new_password1',
          'new_password2',
        ]
    def __init__(self,user, *args, **kwargs):
        self.user = user
        super(ResetPasswordConfirmForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = self.Meta.fields
    def clean_new_password1(self):
        password=self.cleaned_data.get('new_password1')
        if len(password) < 6:
            raise forms.ValidationError(_(u'Password must be 6 characters or more.'))
        elif not re.search('[0-9]',password):
            raise forms.ValidationError(_(u'Please have at least 1 number in your password'))
        elif not re.search('[a-zA-Z]',password):
            raise forms.ValidationError(_(u'Please have at least 1 alphabet in your password'))
        return password
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class AddUserForm(UserForm):
  class Meta(UserForm.Meta):
    pass
  def clean_username(self):
      """
      Validates that the username is alphanumeric and is not already
      in use.

      """
      username = self.cleaned_data['username'].lower()
      try:
          user = AuthUser.objects.get(username__exact=username)
      except AuthUser.DoesNotExist:
        return username
      raise forms.ValidationError(_(u'Already taken. Please choose another one.'))
  
  def clean_email(self):
      email = self.cleaned_data.get('email')
      exist_email = AuthUser.objects.filter(email__exact=email)
      if exist_email:
        raise forms.ValidationError(_(u'Email had been used.Please sign up using different email.'))
      else:
        return email
  
  def save(self,request):
      new_user=super(UserForm,self).save(commit=False)
      new_user.username=new_user.username.lower()
      new_user.slug=slugify(new_user.username)
      new_user.is_active=False
      new_user.set_password(new_user.password)

      #create activation key
      salt = sha.new(str(random.random())).hexdigest()[:5]
      new_user.activation_key = sha.new(salt+new_user.username).hexdigest()

      new_user.save()
      #EMAIL USER OF ACTIVATION KEY
      from django.core.mail import send_mail
      if request.is_secure():
        current_site = 'https://%s' % request.get_host()
      else:
        current_site = 'http://%s' % request.get_host()

      subject = render_to_string('account/activation_email_subject.html',
                                 { 'site': current_site })
      # Email subject *must not* contain newlines
      subject = ''.join(subject.splitlines())

      message = render_to_string('account/activation_email.html',
                                 { 'activation_key': new_user.activation_key,
                                   'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                   'site': current_site })
      if getattr(settings,'EMAIL_HOST',False):
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
      return new_user
  
#    def save(self):
#        import datetime
#        new_store=super(UserForm,self).save()
#        new_store=Store(user=new_store,name="Default",location="Jakarta",contacts=1213,email="example@yahoo.com")
#        new_store.save()
        

class EditUserForm(UserForm):
  class Meta(UserForm.Meta):
    fields=(
          'first_name',
          'last_name',
          'date_of_birth',
          'sex',
          'street_address',
          'country',
          'province',
          'post_code',
          'phone_area_code',
          'telephone',
          'handphone',
          'fax_area_code',
          'fax',
          'email',
          'personal_website',
          'about_me',
          'picture',
    )
    
class UserProfileForm(forms.ModelForm):
    about_me=forms.CharField(widget=forms.Textarea())
    class Meta:
        model=User


class LoginForm(AuthenticationForm):
    def clean(self):
        if self.cleaned_data.get("username"):
            self.cleaned_data["username"] = self.cleaned_data.get("username").lower()
        else:
            self.cleaned_data["username"] = self.cleaned_data.get("username")
        super(LoginForm, self).clean()

class InviteForm(forms.Form):
    email = forms.EmailField(max_length=50,label=_(u'RSVP_To'))
    email2 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    email3 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    email4 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    email5 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    email6 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    email7 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    email8 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    email9 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    email10 = forms.EmailField(max_length=50,label=_(u'RSVP_To'),required=False)
    message = forms.CharField(max_length=1000,widget=forms.Textarea(),label=_(u'message'))
    class Meta:
        fields=['email',
                'email2',
                'email3',
                'email4',
                'email5',
                'email6',
                'email7',
                'email8',
                'email9',
                'email10',
                'message',
               ]

    def __init__(self, *args, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = self.Meta.fields

class EmailShowForm(UserForm):
    class Meta(UserForm.Meta):
        fields=[
          'recaptcha',
        ]
    def __init__(self, *args, **kwargs):
      super(EmailShowForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields