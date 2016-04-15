from django import forms
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _,ugettext
from django.conf import settings

CHOICES = getattr(settings, 'COMPANY_EMAIL', [])

class ContactForm(forms.Form):
    server_email = forms.ChoiceField(widget=forms.widgets.RadioSelect,choices=[(key,_(CHOICES[key][0])) for key in CHOICES],label=_(u'Contact'))
    names = forms.CharField(label=_(u'Name'))
    client_email = forms.EmailField(label=_(u'E-mail'))
    subject = forms.CharField(label=_(u'Subject'))
    message = forms.CharField(label=_(u'Message'),widget=forms.widgets.Textarea)
    cc_myself = forms.BooleanField(label=_(u'Send a copy to my E-mail'),required=False)

    def save(self):
      choice = CHOICES[self.cleaned_data['server_email']]
      name = self.cleaned_data['names']
      subject = 'Fashionment %s - %s' % (choice[0],self.cleaned_data['subject'])
      message = self.cleaned_data['message']
      client_email = self.cleaned_data['client_email']
      cc_myself = self.cleaned_data['cc_myself']

      server_email = choice[1]

      from django.core.mail import EmailMessage

      email_to_company = EmailMessage(
                          subject='%s (by %s)' % (subject,name), 
                          body=message, 
                          to=[server_email], 
#                          bcc=[client_email],
                          headers = {'Reply-To': client_email}
      )
      email_to_company.send()

      if cc_myself:
        email_receipt = EmailMessage(
                            subject='%s (Copy)' % subject, 
                            body=message, 
                            to=[client_email], 
        )
        email_receipt.send()
