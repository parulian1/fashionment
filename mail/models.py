from django.db import models
from django import forms
from accounts.models import User
from store.models import Store
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
#from markdown import markdown
from django.template.defaultfilters import removetags,filesizeformat,mark_safe
from django.conf import settings
from store.postmarkup import render_bbcode

MESSAGE_TYPES =(
        (1,'Pricing'),
        (2,'Delivery'),
        (3,'SizeAndColours'),
        (4,'Others')
    )
    
class Message(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    files = models.FileField(upload_to='mail/files',blank=True)
    def save(self,force_insert=False, force_update=False):
        self.message = removetags(self.message,'script')
        self.message = removetags(self.message,'iframe')
        self.message = mark_safe(render_bbcode(self.message))
        super(Message,self).save(force_insert=force_insert,force_update=force_update)
    def __unicode__(self):
        return unicode("%s %s ") % (self.subject,self.message) #to prevent coerce unicode error

class MessageList(models.Model):
    PRICING = 1
    DELIVERY = 2
    SIZEnCOLOURS = 3
    OTHERS = 4
    COMMENT = 1
    MESSAGE = 2
    MESSAGE_TYPES =(
        (PRICING,'Pricing'),
        (DELIVERY,'Delivery'),
        (SIZEnCOLOURS,'Size&Colours'),
        (OTHERS,'Others'),
    )
    NOTIFICATION_TYPES =(
        (COMMENT,'Comment'),
        (MESSAGE,'Message'),
    )
    thread = models.ForeignKey(Message,verbose_name=_(u'First Message ID'),related_name='thread')
    reply = models.ForeignKey(Message,verbose_name=_(u'Reply Message ID'),related_name='reply',blank=True,null=True)
    from_user = models.ForeignKey(User,verbose_name=_(u'From'),related_name='From')
    to_user = models.ForeignKey(User,verbose_name=_(u'To'),related_name='To')
    message_type = models.IntegerField(choices=MESSAGE_TYPES,default=PRICING)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES,null=True)
    saved = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    notification_read = models.BooleanField(default=False)
    inbox_deleted = models.BooleanField(default=False)
    send_deleted = models.BooleanField(default=False)
    date_send = models.DateTimeField(_(u'Date Sended'),default=datetime.now,null=True)

    class Meta:
        unique_together=(('thread','reply','from_user','to_user'),)

class MessageForm(forms.ModelForm):
    to_user = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'maxlength':1000}))
    message_type = forms.ChoiceField(choices=MESSAGE_TYPES)
    files = forms.FileField(required=False)
    class Meta:
        model = Message
        fields=[
                'to_user',
                'message_type',
                'subject',
                'message',
                'files',
                ]
                
    def __init__(self, *args, **kwargs):
      super(MessageForm, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields
    def clean_to_user(self):
        to_user = self.cleaned_data.get('to_user')
        all_user = User.objects.all()
        exist_user=''
        for user in all_user:
            full_name = user.first_name+" "+user.last_name
            if full_name == to_user:
                exist_user = user
                to_user = user.id
        if not exist_user:
            exist_user = Store.objects.filter(name=to_user)
            if exist_user:
               to_user = exist_user[0].user_id
            else:
               raise forms.ValidationError(_(u'User doesnt exist.'))
        return to_user
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message)>1000:
            raise forms.ValidationError(_(u'The maximum length of message is about 1000 character.'))
        return message
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if len(subject)>100:
            raise forms.ValidationError(_(u'The maximum length of subject is about 100 character.'))
        return subject
    def clean_files(self):
        files = self.cleaned_data.get('files')
        if files:
            if files._size>settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(files._size)))
        return files

class MessageToUser(MessageForm):
    class Meta(MessageForm.Meta):
        fields=[
                'message_type',
                'subject',
                'message',
                'files',
                ]
    def __init__(self, *args, **kwargs):
      super(MessageToUser, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields

class ReplyMessage(MessageForm):
    class Meta(MessageForm.Meta):
        fields=[
                'message',
                'files',
                ]
    def __init__(self, *args, **kwargs):
      super(ReplyMessage, self).__init__(*args, **kwargs)
      self.fields.keyOrder = self.Meta.fields

class SearchMessageForm(forms.Form):
    PRICING = 1
    DELIVERY = 2
    SIZEnCOLOURS = 3
    OTHERS = 4
    MESSAGE_TYPES2 =(
        (None,'----'),

        (PRICING,'Pricing'),
        (DELIVERY,'Delivery'),
        (SIZEnCOLOURS,'Size&Colours'),
        (OTHERS,'Others')
    )
    select = forms.ChoiceField(choices=MESSAGE_TYPES2)
    search = forms.CharField(max_length=50)
    class Meta:
        fields=[
            'select',
            'search',
            ]

    def __init__(self, *args, **kwargs):
        super(SearchMessageForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = self.Meta.fields

class SearchNotificationForm(forms.Form):
    USTORE = 1
    UITEM = 2
    NOTIFICATION_TYPES =(
        (None,'----'),
        (USTORE,'Your Store'),
        (UITEM,'Your Item'),
    )
    select = forms.ChoiceField(choices=NOTIFICATION_TYPES)
    search = forms.CharField(max_length=50)
    class Meta:
        fields=[
            'select',
            'search',
            ]

    def __init__(self, *args, **kwargs):
        super(SearchNotificationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = self.Meta.fields
