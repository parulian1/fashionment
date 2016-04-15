from accounts.forms import AddUserForm,UserProfileForm,EditUserForm,ResetPasswordConfirmForm
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from forms import LoginForm,EmailShowForm
from django.contrib.auth.models import User as AuthUser,check_password
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site
from extra import librecaptcha
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from accounts.models import User
from store.models import Store,Addicted,Rating
from django.contrib.auth.views import password_reset_confirm,logout_then_login
from django.utils.translation import ugettext_lazy as _
from datetime import date
from mail.models import Message,MessageList
from django.utils import simplejson
# Create your views here.



def activate(request, activation_key, template_name='account/activate.html'):
  account = User.objects.activate_user(activation_key)
  return direct_to_template(request,template_name,
      { 'account': account,
      'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
      )
def pass_reset_confirm(request,uidb36,token):
    return password_reset_confirm(request,uidb36=uidb36,token=token,set_password_form=ResetPasswordConfirmForm)


@never_cache
def custom_login(request,template_name='account/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    message=''
    "Displays the login form and handles the login action."
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                """
            temp_active = User.objects.get(username__exact=request.POST.get('username').lower())
            if temp_active:
                if temp_active.active == False:
                    #return HttpResponse('blm login')
                    temp_active.active = True
                    temp_active.save()
                else:
                    #return HttpResponse('udah pernah ada yang login')
                    return HttpResponseRedirect(reverse('auth_login'))
            """
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            #return HttpResponse(redirect_to)
            return HttpResponseRedirect(redirect_to)
    else:
        form = LoginForm(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return direct_to_template(request,'account/login.html',
                                    {
                                         'form': form,
                                         redirect_field_name: redirect_to,
                                         'site_name': current_site.name,
                                         'message':message,
                                    })

def custom_logout(request):
    if request.user.id:
        user = User.objects.get(id=request.user.id)
        user.active = False
        user.save()
    from django.contrib.auth.views import logout
    return logout(request,None,'account/logout.html')

"""
def profile(request):
    if request.method == "POST":
        formprofile = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('add_profile'))
    else:
        formprofile = UserProfileForm()
    return direct_to_template(request,'account/add_profile.html',
                                    {
                                         'formprofile':formprofile,
                                    })
                                    """
def sign_up(request):
    captcha_error=''
    if request.method == "POST":
        add_user_form = AddUserForm(data=request.POST, files=request.FILES, initial={'recaptcha': request.META['REMOTE_ADDR']})
        if add_user_form.is_valid():
                add_user_form=add_user_form.save(request)
                user = get_object_or_404(User,username=add_user_form.username)
                subject = "Thank you for joining Fashionment.com"
                msg="Thank you for joining Fashionment.com. We wish you have an enjoyable time browsing and selling through Fashionment.com.\n What are you waiting for, add your own store now. And do not forget to add up your clothing line by selecting Add Collection under My Store on side bar menu.\n With more lines and items you add, more people will get interested in products you offer.\n Keep check & rechecking your Fashionment Profile and we look forward to see your business success in the future. \n All the best from us. \n Fashionment Team \n For any enquiries please email us at customer-support@fashionment.com \n or call 62.21.6660 2184."
                message = Message.objects.create(subject=subject,message=msg)
                from_user = User.objects.get(id=21)
                MessageList.objects.create(thread=message,reply=None,from_user=from_user,to_user=user,read=False,message_type=4)
                return HttpResponseRedirect(reverse('sign_up_complete'),)
    else:
        add_user_form = AddUserForm()   
    return direct_to_template(request,'account/sign_up.html',
                                    {
                                         'add_user_form':add_user_form,
                                    })

def view_profile(request,user_id):
    addict_to=None
    store_addict=None
    profile=None
    store=None
    rating=None
    owner_flag=0 # default flag for the user who login isnt the owner
    cache_time = 300 # default cache time if the user who login isnt the owner
    if user_id:
        profile = get_object_or_404(User,pk=user_id)
        dob = profile.date_of_birth
        my_age = (((date.today()-dob).days-6)/(365))
        if profile.id != request.user.id:
            
            profile.page_view = profile.page_view+1
            profile.save()
        else:
            owner_flag = 1
            cache_time = 600
        try:
            store = Store.objects.get(user=user_id,deleted=False,user__store__deleted=False)
            
        except:
            store=None
        try:
            
            store1 = Store.objects.get(user=user_id,deleted=False)
            store_addict = Addicted.objects.filter(store=store1.id,deleted=False,store__deleted=False)
            
            rating = Rating.objects.get(store=store1)
            addict_to = Addicted.objects.filter(user=user_id,deleted=False)
        
        except:
            rating =None


           
    #raise Exception(store_addict)
    return direct_to_template(request,'account/view_profile.html',
                                    {
                                        'view_my_profile':profile,
                                        'view_store':store,
                                        'my_addict':store_addict,
                                        'addict_to':addict_to,
                                        'rating':rating,
                                        'my_age':my_age,
                                        'owner_flag':owner_flag,
                                        'cache_time':cache_time,
                                    })
@login_required
def view_my_profile(request):
    profile = get_object_or_404(User,pk=request.user.id)
    dob = profile.date_of_birth
    my_age = (((date.today()-dob).days-6)/(365))
    owner_flag=1 # default flag for the user who login is the owner
    cache_time = 60 # default cache time set to be 0 because it will immidiate change
                    # if the user doesnt 
    try:
        store = Store.objects.get(user=profile.id,deleted=False)
    except:
        store=None
    addict_to = Addicted.objects.filter(user=request.user,deleted=False,store__deleted=False)
    
    try:
        rating = Rating.objects.get(store=request.user.store)
    except:
        rating =None
    if request.user.id:
        try:
            store1 = Store.objects.get(user=request.user.id,deleted=False)
            rating = Rating.objects.get(store=store1)
            store_addict = Addicted.objects.filter(store=store1,deleted=False,store__deleted=False)

            addict_to = Addicted.objects.filter(user=request.user,deleted=False,store__deleted=False)
                
        except:
            rating =None
            store_addict = None

    return direct_to_template(request,'account/view_profile.html',
                                    {
                                        'view_my_profile':profile,
                                        'view_store':store,
                                        'my_addict':store_addict,
                                        'addict_to':addict_to,
                                        'rating':rating,
                                        'my_age':my_age,
                                        'owner_flag':owner_flag,
                                        'cache_time':cache_time,
                                    })
@login_required
def edit_my_profile(request):
    profile = get_object_or_404(User,pk=request.user.id)

    if request.method =="POST":
        form_profile = EditUserForm(data=request.POST,files=request.FILES,instance=profile)
        if form_profile.is_valid():
            form_profile.save()
            return HttpResponseRedirect(reverse('view_my_profile'))
    else:
        form_profile = EditUserForm(instance=profile)
    return direct_to_template(request,'account/edit_profile.html',
                                {
                                    'edit_my_profile_form':form_profile,
                                    'user':profile,
                                    
                                })

"""
def sign_up(request):
    if request.method == "POST":
        add_user_form = AddUserForm(request.POST)
        add_store_form = AddStoreForm(data=request.POST,files=request.FILES)
        if add_user_form.is_valid() and add_store_form.is_valid():
            new_user=add_user_form.save()
            new_store=add_store_form.save(commit=False)
            new_store.user=new_user
            new_store.save()
            new_line=Store.objects.get(pk=new_store.id)
            new_line.line_set.create(store=new_line,line=new_line.name+"'s Line")
            return HttpResponseRedirect(reverse('sign_up'))

    else:
        add_user_form = AddUserForm()
        add_store_form = AddStoreForm()
    return direct_to_template(request,'account/sign_up.html',
                                    {
                                         'add_user_form':add_user_form,
                                         'add_store_form':add_store_form,
                                    })
"""
import base64
import binascii
from Crypto.Cipher import AES
from django.conf import settings
def unpad_string (str):
    # TODO this needs further testing
	numpadchr = str[-1]
	numpad = ord(numpadchr)
	return str[:-numpad]

def dec_string(str):
	key = binascii.unhexlify(settings.MAILHIDE_PRIV_KEY)
	mode = AES.MODE_CBC
	iv = '\000' * 16
	obj = AES.new(key, mode, iv)
	return obj.decrypt(str)

def maihide_decrypts(request):
    erase_string=''
    k= request.GET.get('k')
    c= request.GET.get('c')
    if request.method == "POST":
        form=EmailShowForm(data=request.POST, files=request.FILES, initial={'recaptcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            decode_urlsafe=base64.urlsafe_b64decode(str(c))
            decode_AES=dec_string(decode_urlsafe)
            erase_string=unpad_string(decode_AES)
            if request.is_ajax():

                json_dict={
                'success':True,
                'erase_string':erase_string,
                }
                return HttpResponse(simplejson.dumps(json_dict),mimetype='application/javascript')
        else:
            if request.is_ajax():

                json_dict={
                'field_errors':{
                    'recaptcha':[unicode(error) for error in form.errors['recaptcha']]
                    }
                }
                return HttpResponse(simplejson.dumps(json_dict),mimetype='application/javascript')

    else:
        form=EmailShowForm()
    if request.is_ajax():
        return direct_to_template(request, 'account/show-mail-ajax.html',{
                                                'form':form,
                                                })
    else:
        return direct_to_template(request, 'account/show-mail-not-ajax.html',{
                                                'form':form,
                                                })