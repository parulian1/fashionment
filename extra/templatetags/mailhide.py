import base64
import binascii

from Crypto.Cipher import AES
from django.utils.safestring import mark_safe
from django.conf import settings
from django import template
from django.core.urlresolvers import reverse
register = template.Library()
import math
def pad_string (str, block_size):
	numpad = block_size - (len (str) % block_size)
	return str + numpad * chr (numpad)

def unpad_string (str):
    # TODO this needs further testing
	numpadchr = str[-1]
	numpad = ord(numpadchr)
	return str[:-numpad]

def enc_string(str):
	key = binascii.unhexlify(settings.MAILHIDE_PRIV_KEY)
	mode = AES.MODE_CBC
	iv = '\000' * 16
	obj = AES.new(key, mode, iv)
	return obj.encrypt(str)

def dec_string(str):
	key = binascii.unhexlify(settings.MAILHIDE_PRIV_KEY)
	mode = AES.MODE_CBC
	iv = '\000' * 16
	obj = AES.new(key, mode, iv)
	return obj.decrypt(str)

@register.filter()
def mailhide(value):
    args = {}
    padded_value = pad_string(value, 16)
    encrypted_value = enc_string(padded_value)
    link=reverse('maihide_decrypts')
    args['public_key'] = settings.MAILHIDE_PUB_KEY
    args['encrypted_email'] = base64.urlsafe_b64encode(encrypted_value)
    args['domain'] = value[value.index('@')+1:]
    args['link_reversion']=link
    args['hide_a_little'] = value[0:int(math.ceil(len(value[0:value.index('@')])*0.3))]
    result =  '''%(hide_a_little)s<a class="email_hide" href="%(link_reversion)s?k=%(public_key)s&amp;c=%(encrypted_email)s"
    title="Reveal this e-mail address">...</a>@%(domain)s''' % args
    return mark_safe(result)