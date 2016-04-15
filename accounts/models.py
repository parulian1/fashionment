from django.db import models
from django.contrib.auth.models import User as AuthUser
from datetime import datetime,timedelta
import re
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
# Create your models here.
SHA1_RE = re.compile('^[a-f0-9]{40}$')


SEX_CHOICE =(
(1,'Male'),
(2,'Female'),
)
class CountryAreaCode(models.Model):
    country_name = models.CharField(max_length=100)
    def __unicode__(self):
        return unicode('%s')%(self.country_name)

class ProvinceAreaCode(models.Model):
    province_name = models.CharField(max_length=50)
    country = models.ForeignKey(CountryAreaCode,related_name='country_area')
    def __unicode__(self):
        return unicode('%s') % (self.province_name)

class PhoneAreaCode(models.Model):
    code=models.CharField(max_length=5,unique=True)
    name=models.CharField(max_length=150)
    prov = models.ForeignKey(ProvinceAreaCode,related_name='province_area_code')
    def __unicode__(self):
        return unicode('%s')%(self.code)

class RegistrationManager(models.Manager):
    """
    Custom manager for the ``RegistrationProfile`` model.
    
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.
    
    """
    def activate_user(self, activation_key):
        """
        Validates an activation key and activates the corresponding
        ``AuthUser`` if valid.
        
        If the key is valid and has not expired, returns the ``AuthUser``
        after activating.
        
        If the key is not valid or has expired, returns ``False``.
        
        If the key is valid but the ``AuthUser`` is already active,
        returns ``False``.
        
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                return user
        return False
    
        
    def delete_expired_users(self):
        """
        Removes expired instances of ``RegistrationProfile`` and their
        associated ``AuthUser``s.
        
        Accounts to be deleted are identified by searching for
        instances of ``RegistrationProfile`` with expired activation
        keys, and then checking to see if their associated ``AuthUser``
        instances have the field ``is_active`` set to ``False``; any
        ``AuthUser`` who is both inactive and has an expired activation
        key will be deleted.
        
        It is recommended that this method be executed regularly as
        part of your routine site maintenance; the file
        ``bin/delete_expired_users.py`` in this application provides a
        standalone script, suitable for use as a cron job, which will
        call this method.
        
        Regularly clearing out accounts which have never been
        activated serves two useful purposes:
        
        1. It alleviates the ocasional need to reset a
           ``RegistrationProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-register and
           receive a new activation key.
        
        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.
        
        If you have a troublesome ``AuthUser`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``RegistrationProfile``; an inactive ``AuthUser`` which
        does not have an associated ``RegistrationProfile`` will not
        be deleted.
        
        """
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()

class User(AuthUser):
    MALE = 1
    FEMALE = 2
    VIEWER = 1
    DESIGNER = 2
    SEX_CHOICE =(
    (MALE,'Male'),
    (FEMALE,'Female')
    )
    ACCOUNT_TYPE = (
    (VIEWER,'Viewer/Seller'),
    (DESIGNER,'Designer'),
    )
    sex = models.IntegerField(choices=SEX_CHOICE,default=MALE)
    interest = models.CharField(max_length=50,blank=True)
    about_me = models.CharField(max_length=1000,blank=True)
    picture = models.ImageField(upload_to='account/img',blank=True,null=True)
    phone_area_code = models.ForeignKey(PhoneAreaCode,related_name='phone_area',blank=True,null=True)
    telephone=models.CharField(max_length=20)
    handphone=models.CharField(max_length=20,blank=True,null=True)
    fax_area_code = models.ForeignKey(PhoneAreaCode,related_name='fax_area',blank=True,null=True)
    fax=models.CharField(max_length=20,blank=True,null=True)
    street_address = models.CharField(max_length=1000,blank=True,null=True)
    province = models.ForeignKey(ProvinceAreaCode,related_name='province_area',blank=True,null=True)
    post_code = models.IntegerField(blank=True,null=True)
    country = models.ForeignKey(CountryAreaCode,related_name='country_area_code')
    date_of_birth = models.DateField(default=datetime.now)
    personal_website = models.URLField(blank=True)
    user_addicted = models.ManyToManyField('User',symmetrical=False)
    activation_key = models.CharField(_(u'Activation Key'), max_length=40)
    account_type = models.IntegerField(choices=ACCOUNT_TYPE,default=VIEWER,blank=True)
    page_view = models.IntegerField(default=0)
    #active = models.BooleanField(default=False)
    objects = RegistrationManager()
    def __unicode__(self):
        return self.username
    
    def activate_user(self,activation_key):
    # Make sure the key we're trying conforms to the pattern of a
    # SHA1 hash; if it doesn't, no point trying to look it up in
    # the database.
        if SHA1_RE.search(activation_key):
          try:
              profile = self.activation_key==activation_key
          except self.model.DoesNotExist:
              return False
          if not profile.activation_key_expired():
              user = profile.user
              user.is_active = True
              user.save()
              return user
        return False
        activation_key = activation_key.lower() # Normalize before trying anything with it.

    def activation_key_expired(self):
          """
          Determines whether this ``RegistrationProfile``'s activation
          key has expired.

          Returns ``True`` if the key has expired, ``False`` otherwise.

          Key expiration is determined by the setting
          ``ACCOUNT_ACTIVATION_DAYS``, which should be the number of
          days a key should remain valid after an account is registered.

          """
          expiration_date = timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
          return self.user.date_joined + expiration_date <= datetime.now()
    activation_key_expired.boolean = True

    def about_me_list(self):
        about_me_list=self.about_me.split('\r')
        return about_me_list

    def street_address_list(self):
        street_address_list=self.street_address.split('\r')
        return street_address_list
#    def save(self):
#        from store.models import Store
#        import datetime
#        super(User,self).save()
#        new_store=Store(user=self,name="Default",location="Jakarta",contacts=1213,email="example@yahoo.com",last_updated=datetime.datetime.datetime.now)
#        new_store.save()

