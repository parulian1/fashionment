from models import Magazine
from django import forms

class AdminMagazineForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(),required=False)
    class Meta:
        model = Magazine