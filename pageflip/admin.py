from django.contrib import admin
from pageflip.models import FlashPageFlip

class FlashPageFlipAdmin(admin.ModelAdmin):
    list_display=('pk','slug')
    list_display_links = ('pk','slug')

admin.site.register(FlashPageFlip,FlashPageFlipAdmin)
