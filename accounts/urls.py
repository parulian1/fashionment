from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
# Uncomment the next two lines to enable the admin:


urlpatterns = patterns('',
    #url(r'^add-profile/$','accounts.views.profile',name='add_profile'),
    url(r'^sign-up/$','accounts.views.sign_up',name='sign_up'),
    url(r'^sign-up/complete$','django.views.generic.simple.direct_to_template', {'template': 'result2.html'},name='sign_up_complete'),
    url(r'^login/$','accounts.views.custom_login',{'template_name': 'account/login.html'},name='auth_login'),
     url(r'^logout/$',auth_views.logout,{'template_name': 'account/logout.html'},name='auth_logout'),
    #url(r'^logout/$','accounts.views.custom_logout',name='auth_logout'),
    url(r'^activate/(?P<activation_key>\w+)/$','accounts.views.activate',name='registration_activate'),
    url(r'^my-profile/$','accounts.views.view_my_profile',name='view_my_profile'),
    url(r'^profile/(?P<user_id>\d+)/','accounts.views.view_profile',name='view_profile'),
    url(r'^edit-profile/$','accounts.views.edit_my_profile',name='edit_profile'),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',name="forgot_password"),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'accounts.views.pass_reset_confirm',name='pass_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^mailhide/$','accounts.views.maihide_decrypts',name='maihide_decrypts'),
)
