from django import forms

class FormAddZipFile(forms.Form):
    file  = forms.FileField()

class FormAddZipFileManual(forms.Form):
    file_path  = forms.CharField(max_length=100)