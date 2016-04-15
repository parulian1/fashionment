from django import template
from datetime import datetime

register = template.Library()

def upgrade_browser(context):
    browser=context['request'].META.get('HTTP_USER_AGENT','Nothing in http user agent')
    bool='MSIE' in browser
    return {'IE':bool}

register.inclusion_tag('extra/upgrade_browser.html', takes_context=True)(upgrade_browser)
