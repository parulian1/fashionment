from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
# truncate after a certain number of characters
def truncatechar(value, arg):
    if len(value) < arg:
        return value
    else:
        return value[:arg] + '...'

@register.filter
def truncatecharnotags(value, arg):
    value = strip_tags(value)
    if len(value) < arg:
        return value
    else:
        return value[:arg] + '...'


from extra.BeautifulSoup import BeautifulSoup, Comment
import re

def sanitize(value, allowed_tags):
    """Argument should be in form 'tag2:attr1:attr2 tag2:attr1 tag3', where tags
    are allowed HTML tags, and attrs are the allowed attributes for that tag.
    """
    js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
    allowed_tags = [tag.split(':') for tag in allowed_tags.split()]
    allowed_tags = dict((tag[0], tag[1:]) for tag in allowed_tags)

    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    for tag in soup.findAll(True):
        if tag.name not in allowed_tags:
            tag.hidden = True
        else:
            tag.attrs = [(attr, js_regex.sub('', val)) for attr, val in tag.attrs
                         if attr in allowed_tags[tag.name]]

    return soup.renderContents().decode('utf8')
register.filter(sanitize)