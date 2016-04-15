from models import Magazine
from django.contrib import admin
from forms import AdminMagazineForm

class MagazineAdmin(admin.ModelAdmin):
    form=AdminMagazineForm
    list_display=('pk','title','image')
    list_display_links=('pk','title',)
    fieldsets=(
      (None,{'fields':('title','description')}),
      ('URL OR Download File',{
        'fields':('url','download_file',)}),
      ('Image ',{
        'fields':('image',)}),
      ('Image for fashion facts',{
        'fields':('fact_img',)}),
      (None,{
        'fields':('deleted',)}),
      ('Show at Index',{
        'fields':('index',)}),
    )
    
admin.site.register(Magazine,MagazineAdmin)