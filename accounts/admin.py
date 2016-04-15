from django.contrib import admin
from models import CountryAreaCode,ProvinceAreaCode,PhoneAreaCode,User
from store.models import Store,LineCategory,Line,Item,Addicted,Comment,View,CommentNumber,Rating,RatingCounter,Compare_List,Currency
from django.template.defaultfilters import slugify
from mail.models import Message,MessageList
class PhoneAreaCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name','prov')

class CountryAreaCodeAdmin(admin.ModelAdmin):
    list_display = ('id','country_name')

class ProvinceAreaCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'province_name','country')

class LineCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','__unicode__')

class LineAdmin(admin.ModelAdmin):
    list_display = ('id', '__unicode__')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', '__unicode__')

class UserAdmin(admin.ModelAdmin):
  #prepopulated_fields = {'slug': ('name',)}
  list_display = ('id','__unicode__')

admin.site.register(CountryAreaCode,CountryAreaCodeAdmin)
admin.site.register(ProvinceAreaCode,ProvinceAreaCodeAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(PhoneAreaCode,PhoneAreaCodeAdmin)
admin.site.register(LineCategory,LineCategoryAdmin)
admin.site.register(Line,LineAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(Addicted)
admin.site.register(Comment)
admin.site.register(View)
admin.site.register(CommentNumber)
admin.site.register(Rating)
admin.site.register(RatingCounter)
admin.site.register(Compare_List)
admin.site.register(Message)
admin.site.register(MessageList)
admin.site.register(Currency)
