#    Copyright (c) 2007 Renzo Carbonara <gnuk0001 at gmail dot com>
#    Based on the original implementation by Ben Maurer <support at recaptcha net>
#    
#    MIT/X11 License:
#    
#    Permission is hereby granted, free of charge, to any person
#    obtaining a copy of this software and associated documentation
#    files (the "Software"), to deal in the Software without
#    restriction, including without limitation the rights to use,
#    copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the
#    Software is furnished to do so, subject to the following
#    conditions:
#    
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#    OTHER DEALINGS IN THE SOFTWARE.

import urllib2, urllib
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
import re

RECAPTCHA_PUBLIC = getattr(settings,'RECAPTCHA_PUBLIC','6Lc49AUAAAAAAKCmiwBJumY1rsN70R4ijxMyqjat')
RECAPTCHA_PRIVATE = getattr(settings,'RECAPTCHA_PUBLIC','6Lc49AUAAAAAANwTboQssL6EKMf_5HiP7h6kfq1q')

if RECAPTCHA_PUBLIC and RECAPTCHA_PRIVATE:
    API_SSL_SERVER = "https://api-secure.recaptcha.net"
    API_SERVER = "http://api.recaptcha.net"
    VERIFY_SERVER = "api-verify.recaptcha.net"
    AJAX_JS = 'http://api.recaptcha.net/js/recaptcha_ajax.js'
else:
    API_SSL_SERVER = ""
    API_SERVER = ""
    VERIFY_SERVER = ""
    AJAX_JS = ""

# customization (first value is used as fallback)
VALID_THEMES = ('red', 'white', 'blackglass', 'clean', 'custom')
VALID_LANGS = ('en', 'nl', 'fr', 'de', 'pt', 'ru', 'es', 'tr')


class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def displayhtml (public_key, name, ajax_js=AJAX_JS, use_ssl=False, error=None,
                 theme='red',lang='en', tabindex=0,
                 custom_theme_widget='null'):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)
    theme -- Color Theme
    lang -- Language Code
    tabindex -- Tabindex to use for the field
    custom_theme_widge -- Custom theme widget (A string with the ID of a DOM element)
    
    More info: http://recaptcha.net/apidocs/captcha/client.html
    """

    error_param = ''
    if error:
	error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    theme = (VALID_THEMES[0], theme) [ theme in VALID_THEMES ]
    labg = (VALID_LANGS[0], lang) [ lang in VALID_LANGS ]
    html = u"""
<script type="text/javascript" src="%(ajax_js)s"></script>

<div id="recaptcha_object">
  <iframe src="%(ApiServer)s/noscript?k=%(PublicKey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='%(name)s' value='manual_challenge' />
</div>
<script>
  var recaptcha_object = document.getElementById('recaptcha_object')

  var recaptcha_image=document.createElement('div')
  recaptcha_image.className='recaptcha_image'
  recaptcha_image.setAttribute('style','width:300px;height:57px')

  var recaptcha_image_holder = document.createElement('div')
  recaptcha_image_holder.className='recaptcha_image_holder'
  recaptcha_image_holder.style.overflow = 'hidden'
  recaptcha_image_holder.style.height = '1%%'

  var recaptcha_response_field = document.createElement('input')
  recaptcha_response_field.setAttribute('name',"%(name)s")
  recaptcha_response_field.style.width = '300px'

  recaptcha_object.parentNode.insertBefore(recaptcha_image_holder,recaptcha_object)
  recaptcha_image_holder.appendChild(recaptcha_image)
  recaptcha_object.parentNode.insertBefore(recaptcha_response_field,recaptcha_object)
  
  recaptcha_object.parentNode.removeChild(recaptcha_object) //remove recaptcha object

//LOAD RECAPTCHA IMAGE

  function loadRecaptchaImage(RecaptchaState0,recaptcha_image0){
      var recaptcha_image = recaptcha_image0
      var RecaptchaState = RecaptchaState0
      //LOAD RECAPTCHA IMAGE
      var imageurl = RecaptchaState.server + 'image?c=' + RecaptchaState.challenge;
      recaptcha_image.innerHTML = "<img style='display:block;' height='57' width='300' src='" + imageurl + "'/>";
  }
  //LOAD RECAPTCHA CHALLENGE FIELD
  var recaptcha_challenge_field = document.createElement('input')
  recaptcha_challenge_field.setAttribute('name','recaptcha_challenge_field')
  recaptcha_challenge_field.setAttribute('type','hidden')
  recaptcha_response_field.parentNode.insertBefore(recaptcha_challenge_field,recaptcha_response_field.nextSibling)

  Recaptcha.theme='custom'
  Recaptcha.recaptcha_image = recaptcha_image
  Recaptcha.recaptcha_challenge_field = recaptcha_challenge_field
  Recaptcha.challenge_callback=function(){
      //UPDATE RECAPTCHA CHALLENGE FIELD
      Recaptcha.recaptcha_challenge_field.setAttribute('value',RecaptchaState.challenge)
      loadRecaptchaImage(RecaptchaState,Recaptcha.recaptcha_image)
      return 1
  }
  Recaptcha.finish_reload=function(new_challenge){
      //UPDATE RECAPTCHA CHALLENGE FIELD
      RecaptchaState.challenge = new_challenge
      Recaptcha.recaptcha_response_field.value = ''
      Recaptcha.recaptcha_challenge_field.setAttribute('value',RecaptchaState.challenge)
      loadRecaptchaImage(RecaptchaState,Recaptcha.recaptcha_image)
      return 1
  }
  Recaptcha._call_challenge("%(PublicKey)s")

  var reload_button = document.createElement('a')
  reload_button.setAttribute('href','#')
  reload_button.className = 'reload_recaptcha'
  reload_button.innerHTML='%(reload_image)s'
  reload_button.recaptcha_image = recaptcha_image
  reload_button.recaptcha_response_field = recaptcha_response_field
  reload_button.recaptcha_challenge_field = recaptcha_challenge_field
  reload_button.onclick=function(e){
    if(!e){
        //if ie
        event.returnValue=false
    }
    else{
        e.preventDefault()
    }
    this.recaptcha_image.innerHTML=''
    Recaptcha.recaptcha_image = this.recaptcha_image
    Recaptcha.recaptcha_response_field = this.recaptcha_response_field
    Recaptcha.recaptcha_challenge_field = this.recaptcha_challenge_field
    var scriptURL = RecaptchaState.server + "reload?c=" + RecaptchaState.challenge + "&k=" + RecaptchaState.site + "&type=image"+"&reason=r" 
    Recaptcha._add_script(scriptURL)
    
  }
  recaptcha_image.parentNode.insertBefore(reload_button,recaptcha_image.nextSibling)
</script>
""" % {
        'ApiServer'          : server,
        'PublicKey'          : public_key,
        'ErrorParam'         : error_param,
        'theme'              : theme,
        'lang'               : lang,
        'tabindex'           : tabindex,
        'ajax_js'            : ajax_js,
        'custom_theme_widget': custom_theme_widget, 
        'reload_image'       : _('Reload Image'),
        'name'               : name,
      }

    return html

def submit (recaptcha_challenge_field,
            recaptcha_response_field,
            private_key,
            remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len (recaptcha_response_field) and len (recaptcha_challenge_field)):
        return RecaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')
    
    params = urllib.urlencode ({
        'privatekey': private_key,
        'remoteip'  : remoteip,
        'challenge' : recaptcha_challenge_field,
        'response'  : recaptcha_response_field.encode('utf-8'),
        })

    request = urllib2.Request (
        url = "http://%s/verify" % VERIFY_SERVER,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )
    
    httpresp = urllib2.urlopen (request)

    return_values = httpresp.read ().splitlines ();
    httpresp.close();

    return_code = return_values [0]

    if (return_code == "true"):
        return RecaptchaResponse (is_valid=True)
    else:
        return RecaptchaResponse (is_valid=False, error_code = return_values [1])

class ReCaptcha(object):
    def __init__(self):
        response = urllib2.urlopen('http://api.recaptcha.net/noscript?k=%s' % RECAPTCHA_PUBLIC)
        html = response.read()
        response.close()

        pattern = r'recaptcha_image_cell.*?src="(.*?)"'
        matches = re.search(pattern, html)
        self.image_url = 'http://api.recaptcha.net'+matches.group(1)

        pattern = r'recaptcha_challenge_field.*?value="(.*?)"'
        matches = re.search(pattern, html)
        self.challenge_value = matches.group(1) 
