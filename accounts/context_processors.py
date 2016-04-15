from ads.models import Ad,AdForIndex
from store.models import Store,Line,Item
from mail.models import MessageList
from accounts.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime
import random

def login_form(request):
  from django.contrib.auth.forms import AuthenticationForm
  return {'login_form':AuthenticationForm()}

def user(request,):
  user=''
  store=''
  lines=''
  inbox = MessageList.objects.filter(to_user=request.user.id,read=False,inbox_deleted=False,saved=False,reply=None,notification_type__isnull=True).count()
  notification = MessageList.objects.filter(to_user=request.user.id,reply=None,notification_type__isnull=False,inbox_deleted=False,send_deleted=False).count()
  all_ad = Ad.objects.all().order_by('id')
  left_ad=all_ad.filter(ad_status=1)
  bottom_ad = all_ad.filter(ad_status=3)
  if bottom_ad:
      bottom_ad=bottom_ad[0]
  ads_index = AdForIndex.objects.all()
  total_store = Store.objects.filter(deleted=False).count()
  total_item = Item.objects.filter(deleted=False,line__store__deleted=False).count()
  if request.user.id:
    user=get_object_or_404(User,pk=request.user.id)
    try:
        store = Store.objects.get(user=user,deleted=False)
        lines = Line.objects.filter(store=store)
    except:
      store=None
      lines=''

  for line in lines:
    line.my_items = line.item_set.filter(deleted=False).order_by('-set_primary_date','-id')
  comment_ad = Ad.objects.filter(ad_status=2).order_by('id')
  viewed_ad2=''
  if not request.session.get('randomed'):
        randomed_ad = random.sample(comment_ad,comment_ad.count())
        if randomed_ad:
            viewed_ad2 = randomed_ad[0]
            viewed_ad2.date_rotation = datetime.now()
            viewed_ad2.save()
  else:
        comment_ad = comment_ad.order_by('date_rotation')
        if comment_ad:
            viewed_ad2=comment_ad[0]
            viewed_ad2.date_rotation = datetime.now()
            viewed_ad2.save()
  request.session['randomed']=True
  
  return {'user':user,'store2':store,'line_data':lines,'left_ad':left_ad,'bottom_ad':bottom_ad,'ads_index':ads_index,'total_store':total_store,'total_item':total_item,'inbox':inbox,'viewed_ad2':viewed_ad2,'notification':notification,}