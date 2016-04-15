from store.forms import CommentForm,ItemForm,EditItemForm,EditStoreForm, LineForm, AddStoreForm,SearchStoreForm,SearchItemForm,VoucherForm,EditLineForm
from store.models import Store,Line,Addicted,Item,Comment,Compare_List,View,CommentNumber,Rating,RatingCounter,LineCategory
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect,HttpResponse, Http404,HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from accounts.models import User
from accounts.forms import InviteForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from datetime import datetime,date
from mail.models import Message,MessageList,MessageToUser
import random
from django.core.mail import EmailMessage
from django.template.defaultfilters import slugify,truncatewords
from coltrane.models import FashionFacts
from django.utils import simplejson
from horoscope.models import Horoscope
from django.views.decorators.cache import cache_page
from django.core import serializers
from django.utils.text import capfirst

@login_required
def add_store(request):
    user = get_object_or_404(User,pk=request.user.id)
    if request.method == "POST":
        form = AddStoreForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            save2=form.save(commit=False)
            save2.user=user
            save2.slug = slugify('%s'%(save2.name))
            save2.save()
            return HttpResponseRedirect(reverse('view_my_profile'))
    else:
        form = AddStoreForm()
    return direct_to_template(request,'store/add_store.html',{
                                'add_store_form':form,
                                'user_data':user,
                            })
                            
@login_required
def edit_store(request):
    store = get_object_or_404(Store,user=request.user,deleted=False)
    if request.method == "POST":
        form = EditStoreForm(data=request.POST,files=request.FILES,instance=store)
        if form.is_valid():
            save1=form.save(commit=False)
            save1.last_updated=datetime.now()
            save1.slug=slugify('%s'%(save1.name))
            save1.save()
            fans = Addicted.objects.filter(store=store,deleted=False)
            subject = str(store.name)+" has updated at "+store.last_updated.strftime('%Y-%b-%d')
            message = "Hello Fashion Fans "+store.name+" has recently updated at "+store.last_updated.strftime('%Y-%b-%d')+". See the changes of the store by log in into your fashion account. Regards, Fashion Teams"
            for fan in fans:
                msg=Message.objects.create(subject=subject,message=message)
                MessageList.objects.create(thread=msg,reply=None,from_user=store.user,to_user=fan.user,message_type=4)
            redirect = HttpResponseRedirect(reverse('view_store'))
            redirect['cache-control']='no-cache'
            return redirect

    else:
        form = EditStoreForm(instance=store)

    return direct_to_template(request,'store/edit_store.html',{
                                'form':form,
                            })

def view_store(request,slug=None):
    formcomment=None
    comment=None
    lines = None
    viewed = None
    rate_date = None
    rating =None
    flag =0
    addict=None
    store_addict = None
    design_flg = 0
    rating_count = ''
    target=[]
    owner_flag=0 # default flag for the user who login isnt the owner
    cache_time = 1800 # default cache time if the user who login isnt the owner
    if slug:
        store = get_object_or_404(Store,slug=slug,deleted=False)
        comment =Comment.objects.filter(store=store,store__deleted=False)

        try:
            store_addict = Addicted.objects.filter(store__slug=slug,user__store__deleted=False,deleted=False)
            rating_count = RatingCounter.objects.filter(store=store)
        except:
            store_addict = None
        try:
            addict = Addicted.objects.filter(user=request.user,store=store,store__deleted=False ,deleted=False)
        except:
            addict = None
        if store.user.id != request.user.id:
            owner_flag = 1
            cache_time = 600
            try:
                rating = Rating.objects.get(store=store)
                try:
                    rate_date = RatingCounter.objects.get(user=request.user,pub_date=date.today(),store=store)
                    if rate_date:
                        flag = 1
                except:
                    rate_date = None
                    flag =0
            except:
                rating =None
        else:
            flag=1
        if store.user.id != request.user.id:
            try:
                view = View.objects.get(store=store,store__deleted=False)
                view.count = view.count + 1
                view.save()
            except:
                View.objects.create(store=store,count=1)

    else:
        
        user_data = get_object_or_404(User,pk=request.user.id)
        try:
            store = Store.objects.get(user=user_data,deleted=False)
        except:
            store = None
        if store:
            comment =Comment.objects.filter(store=store)
            try:
                rating_count = RatingCounter.objects.filter(store=store)
                store_addict = Addicted.objects.filter(store=store,user__store__deleted=False,deleted=False )
            except:
                store_addict = None
            if store.user.id != request.user.id:
                try:
                    rating = Rating.objects.get(store=store)
                    try:
                        rate_date = RatingCounter.objects.get(user=request.user,pub_date=date.today(),store=store)

                        if rate_date:
                            flag = 1
                    except:
                        rate_date = None
                        flag =0
                except:
                    rating =None
            else:
                flag=1
    if request.method=="POST":
        formcomment=CommentForm(data=request.POST)
        if formcomment.is_valid():
            www="http://www.fashionment.com"+reverse('view_stores',args=(slug,))
            subject = "User "+str(request.user.username)+" has sent you a comment about your store "
            message = "User "+str(request.user.username)+" has sent you a comment about "+str(store.name)+". Read further information by log in into your fashion account and go to this url  "+www+"."
            msg_to_mail="User "+str(request.user.username)+" has sent you message about "+str(store.name)+" store. \n Read further information by log in into your fashion account and go to this url "+www+". \n Regards , \n Fashion Team. "
            new_msg=Message.objects.create(subject=subject,message=message)
            comment1=formcomment.save(commit=False)
            comment1.user_id=request.user.id
            comment1.store_id=store.id
            comment1.item_id=None
            comment1.date_added = datetime.now()
            comment1.save()

            if store.user.id != request.user.id:
                user= User.objects.get(id=request.user.id)
                MessageList.objects.create(thread=new_msg,reply=None,from_user=user,to_user=store.user,message_type=4,notification_type=1)
                email = EmailMessage(
                                 subject=subject,
                                 body=msg_to_mail,
                                 from_email=request.user.email,
                                 to=[store.user.email],
                                )
            else:
                store_comment = Comment.objects.filter(store=store).exclude(user__id=request.user.id)
                for target_user in store_comment:
                    to_user = User.objects.get(id=target_user.user.id)
                    MessageList.objects.create(thread=new_msg,reply=None,from_user=store.user,to_user=target_user.user,message_type=4,notification_type=1)

                    if target:
                        for temporary in target:
                            if not temporary in target:
                                target.append(to_user.email)
                    else:
                        target.append(to_user.email)
                email = EmailMessage(
                                 subject=subject,
                                 body=msg_to_mail,
                                 from_email=request.user.email,
                                 to=target,
                                )
            email.send()
            slug=store.slug
            try:
                comment_plus = CommentNumber.objects.get(store=store,store__deleted=False)
                comment_plus.count = comment_plus.count+1
                comment_plus.save()
            except:
                CommentNumber.objects.create(store=store,count=1)
            request.user.message_set.create(message="Please wait for few minutes before we upload your comment.")
            return HttpResponseRedirect(reverse('view_stores',args=(slug,)))
    else:
        formcomment = CommentForm()
    lines = Line.objects.filter(store=store)

    if lines.count()>2:
        design_flg = 1
    else:
        design_flg = 0
    for line in lines:
        line.my_items = line.item_set.filter(line__store=store,deleted=False).order_by('-set_primary_date','-id')
    if not request.user.id:
        flag=1
    data = store
    if not store:
        comment = ''
    paginator = Paginator(comment,10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        comment_list = paginator.page(page)
    except(EmptyPage, InvalidPage):
        comment_list = paginator.page(paginator.num_pages)
    return direct_to_template(request,'store/view_store.html',{
                                'view_store':store,
                                'form':formcomment,
                                'comment':comment,
                                'my_addict':store_addict,
                                'line_data':lines,
                                'line_dummy':lines,
                                'view':viewed,
                                'rating':rating,
                                'addict':addict,
                                'rate_date':rate_date,
                                'flag':flag,
                                'design_flg':design_flg,
                                'rating_counter':rating_count,
                                'page_obj':comment_list,
                                'paginator':paginator,
                                'data':data,
                                'owner_flag':owner_flag,
                                'cache_time':cache_time,
                            })
@login_required
def remove_store(request):
    user = get_object_or_404(User,pk=request.user.id)
    try:
        remove = Store.objects.get(user=user,deleted=False)
    except:
        raise Http404
    remove.deleted = True
    remove.save()
    return HttpResponseRedirect(reverse('view_my_profile'))

def view_comment(request,slug,store_id=None):
    if slug=="store":
        if store_id:
            store = get_object_or_404(Store,pk=store_id)
            comment = Comment.objects.filter(store=store,store__deleted=False).order_by('-id')
        else:
            user_data = get_object_or_404(User,pk=request.user.id)
            store = get_object_or_404(Store,user=user_data)
            comment =Comment.objects.filter(store=store,store__deleted=False).order_by('-id')
        
    elif slug=="item":
        if store_id:
            store = get_object_or_404(Item,pk=store_id)
            comment = Comment.objects.filter(item=store,item__line__store__deleted=False,item__deleted=False).order_by('-id')
    else:
        raise Http404
    data = store
    if comment:
        total_comment = comment.count()
    else:
        total_comment = 0
    paginator = Paginator(comment,10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        comment_list = paginator.page(page)
    except(EmptyPage, InvalidPage):
        comment_list = paginator.page(paginator.num_pages)
    #return HttpResponse(comment_list)
    return direct_to_template(request,'store/comment.html',{'page_obj':comment_list,'paginator':paginator,'data':data,'page':page,'total_comment':total_comment,'slug':slug,'id':store_id})

def list_store(request,type=None,alphabet=None):
    temp =[]
    store_list = ''
    flag = 0
    flg = 0
    code_flg = 0
    gets = {}
    gets_string=''
    array = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0-9']
    form = SearchStoreForm()
    form2 = SearchItemForm()
    dict = {
            'keyword':'store__name__icontains',
            'category':'category',
            'line':'line'
            }
    dict2 = {
            'keyword':'name__icontains'
            }
    temp_store = None
    temp_store2 = None
    new_stores = None
    new_arrival = None
    corrected_query=''
    kwargs_dict_count = 0
    kwargs_dict2_count = 0
    temporary = '' # temporary for store indexing result
    if not type:
        type="store"
    object = []
    loop = 1
    divide = 5
    link_back=False
    div_id=0
    if type=="store":
        object=[]
        if not alphabet:
            
            for char in array:
                if char!="0-9":
                    temporary = Store.objects.filter(deleted=False,name__istartswith=str(char),user__account_type=1).order_by('name')
                else:
                    from django.db.models import Q
                    args = Q()
                    temporary = Store.objects.filter(args)
                    for i in xrange(0,10):
                        args = args|Q(deleted=False,name__startswith=i)
                    temporary = temporary.filter(args)
                if char=="0-9":
                    link_back=True
                elif loop %15==0:
                    link_back=True
                    div_id+=1
                else:
                    link_back=False
                if loop % divide ==0:
                    clear=True
                else:
                    clear = False

                loop+=1
                object.append({'alphabet':char,'object':temporary,'clear':clear,'link_back':link_back,'div_id':div_id})
        else:
            if alphabet=="0-9":
                from django.db.models import Q
                args = Q()
                temporary = Store.objects.filter(args)
                for i in xrange(0,10):
                    args = args|Q(deleted=False,name__startswith=i)
                temporary = temporary.filter(args)
            else:
                temporary = Store.objects.filter(name__istartswith=alphabet,deleted=False,user__account_type=1).order_by('name')
            clear=False
            object.append({'alphabet':alphabet,'object':temporary,'clear':clear})
    elif type=="collection":
        object=[]
        #return HttpResponse('harusnya dimari')
        array=LineCategory.objects.all()
        if not alphabet:
            for char in array:
                temporary = Line.objects.filter(store__deleted=False,category=char).order_by('line')
                temporary_line = temporary
                for temp_line in temporary_line:
                    show = False
                    same_name_filter = temporary.filter(line__startswith=temp_line.line)
                    temp_line.same_name_count = same_name_filter.count()
                    if temp_line.same_name_count>1:
                        if temp_line.id==same_name_filter[0].id:
                            show = True
                    else:
                            show=True
                    temp_line.show=show
                if loop % divide == 0:
                    clear = True
                else:
                    clear = False
                loop+=1
                object.append({'alphabet':char,'object':temporary_line,'clear':clear,'link_back':link_back,'div_id':div_id})
        else:
            temporary = Line.objects.filter(category__name=alphabet,store__deleted=False).order_by('line')
            clear=False
            object.append({'alphabet':alphabet,'object':temporary,'clear':clear,'link_back':link_back,'div_id':div_id})
    elif type=="designer":
        object=[]
        if not alphabet:
            for char in array:
                temporary = Store.objects.filter(deleted=False,name__istartswith=str(char),user__account_type=2).order_by('name')
                if char=="0-9":
                    link_back=True
                elif loop %15==0:
                    link_back=True
                    div_id+=1
                else:
                    link_back=False
                if loop % divide ==0:
                    clear=True
                else:
                    clear = False

                loop+=1
                object.append({'alphabet':char,'object':temporary,'clear':clear,'link_back':link_back,'div_id':div_id})
        else:
            if alphabet=="0-9":
                from django.db.models import Q
                args = Q()
                temporary = Store.objects.filter(args)
                for i in xrange(0,10):
                    args = args|Q(deleted=False,name__startswith=i,user__account_type=2)
                temporary = temporary.filter(args)
            else:
                temporary = Store.objects.filter(name__istartswith=alphabet,deleted=False,user__account_type=2).order_by('name')
            clear=False
            object.append({'alphabet':alphabet,'object':temporary,'clear':clear})
    #raise Exception(object)
    if request.GET and request.method == "GET":
      gets=request.GET.copy()
      kwargs = {}
      kwargs2 = {}
      form = SearchStoreForm(request.GET)
      for field in request.GET.items():
              if field[0]!='page' :
                  if field[0]!='submit':
                     if field[1]:
                          if dict.has_key(field[0]):
                              if field[0]=='line':
                                  line_name = Line.objects.get(id=field[1]).line
                                  kwargs[str(dict[field[0]])]=line_name
                              else:
                                  kwargs[str(dict[field[0]])] = field[1]
                              kwargs_dict_count+=1
                          if dict2.has_key(field[0]):
                              kwargs2[str(dict2[field[0]])]=field[1]
                              kwargs_dict2_count+=1
                          gets[field[0]]=field[1]

      if kwargs_dict_count>kwargs_dict2_count:
            temp_store = Line.objects.filter(store__deleted=False,**kwargs)
            for store in temp_store:
                temp.append(store.store.id)
      else:
            temp_store2 = Store.objects.filter(deleted=False,**kwargs2)
            for store2 in temp_store2:
               temp.append(store2.id)
          #return HttpResponse(temp)
      store_list = Store.objects.filter(id__in=temp,user__account_type=1)
      for store in store_list :
            try:
                addict = Addicted.objects.get(store=store,user=request.user,deleted=False)
            except:
                addict = ''
            if addict :
                store.addicted = True
            else:
                store.addicted = False
      if store_list.count() > 3:
            flg = 1
      else:
            flg = 0
      code_flg = 1
      gets_string="&".join(["%s=%s" % (k, v) for k, v in gets.items()])
    paginator = Paginator(store_list,5)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        stores = paginator.page(page)
    except:
        stores = paginator.page(paginator.num_pages)
    return direct_to_template(request,'store/search_base.html',{'paginator':paginator,'page_obj':stores,'form':form,'form2':form2,'flag':flag,'new_stores':new_stores,'new_arrival':new_arrival,'temp_flg':flg,'code_flg':code_flg,'gets_string':gets_string,'corrected_query':corrected_query,'array':array,'type':type,'object':object,})

def list_designer(request):
    temp =[]
    store_list = ''
    flag = 0
    flg = 0
    code_flg = 0
    gets = {}
    designer_flg = 1
    gets_string=''
    form = SearchStoreForm()
    form2 = SearchItemForm()
    dict = {
            'keyword':'store__name__icontains',
            'category':'category',
            'line':'line'
            }
    dict2 = {
            'keyword':'name__icontains'
            }
    temp_store = None
    temp_store2 = None
    new_stores = None
    new_arrival = None
    corrected_query=''
    kwargs_dict_count = 0
    kwargs_dict2_count = 0
    if request.GET and request.method == "GET":
      gets=request.GET.copy()
      kwargs = {}
      kwargs2 = {}
      form = SearchStoreForm(request.GET)
      for field in request.GET.items():
              if field[0]!='page' :
                  if field[0]!='submit':
                     if field[1]:
                          if dict.has_key(field[0]):
                              if field[0]=='line':
                                  line_name = Line.objects.get(id=field[1]).line
                                  kwargs[str(dict[field[0]])]=line_name
                              else:
                                  kwargs[str(dict[field[0]])] = field[1]
                              kwargs_dict_count+=1
                          if dict2.has_key(field[0]):
                              kwargs2[str(dict2[field[0]])]=field[1]
                              kwargs_dict2_count+=1
                          gets[field[0]]=field[1]

      if kwargs_dict_count>kwargs_dict2_count:
            temp_store = Line.objects.filter(store__deleted=False,**kwargs)
            for store in temp_store:
                temp.append(store.store.id)
      else:
            temp_store2 = Store.objects.filter(deleted=False,**kwargs2)
            for store2 in temp_store2:
               temp.append(store2.id)
          #return HttpResponse(temp)
      store_list = Store.objects.filter(id__in=temp,user__account_type=2)
      for store in store_list :
            try:
                addict = Addicted.objects.get(store=store,user=request.user,deleted=False)
            except:
                addict = ''
            if addict :
                store.addicted = True
            else:
                store.addicted = False
      if store_list.count() > 3:
            flg = 1
      else:
            flg = 0
      code_flg = 1
      gets_string="&".join(["%s=%s" % (k, v) for k, v in gets.items()])
    paginator = Paginator(store_list,5)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        stores = paginator.page(page)
    except:
        stores = paginator.page(paginator.num_pages)
    return direct_to_template(request,'store/search_base.html',{'paginator':paginator,'page_obj':stores,'form':form,'form2':form2,'flag':flag,'new_stores':new_stores,'new_arrival':new_arrival,'temp_flg':flg,'code_flg':code_flg,'gets_string':gets_string,'corrected_query':corrected_query,'designer_flag':designer_flg})

def list_item(request):
    temp = []
    store_list = ''
    flag = 1
    form = SearchStoreForm()
    form2 = SearchItemForm()
    flg = 0
    code_flg = 0
    gets={}
    get_string=''
    dict = {
            'keywords':'item__icontains',
            'gender':'gender',
            'availability':'availability',
            'category':'line__category'
            }
    temp_store2 = None
    if request.GET and request.method == "GET" :
        kwargs = {}
        form2 = SearchItemForm(request.GET)

        for field in request.GET.items():

          if field[0]!='submit2':
             if field[1]:
                  if dict.has_key(field[0]):
                      kwargs[str(dict[field[0]])] = field[1]
                  gets[field[0]]=field[1]
        get_string="&".join(["%s=%s" % (k, v) for k, v in gets.items()])
        if kwargs :
            temp_store2 = Item.objects.filter(line__store__deleted=False,deleted=False,**kwargs)
            for data in temp_store2 :
                temp.append(data.id)
        store_list = Item.objects.filter(id__in=temp)
        for store in store_list :
            try:
                 addict = Addicted.objects.get(store=store.line.store,user=request.user,deleted=False)
            except:
              addict = ''
            if addict :
                store.addicted = True
            else:
                store.addicted = False
        if store_list.count() > 3:
            flg = 1
        else:
            flg = 0
        code_flg = 1
    """testing index using raw sql query
      cursor = connection.cursor()
      cursor.execute("SELECT s.id FROM store_store s,store_line l where s.name like '%s' or l.line like '%s' "% (str('%%'+field[1]+'%%'),str('%%'+field[1]+'%%')))
      row = cursor.fetchall()
      for data in row :
           temp.append(data[0])
      store_list = Store.objects.filter(id__in=temp)
    """
    new_stores = Store.objects.filter(deleted=False).order_by('-id')
    new_arrival = Item.objects.filter(line__store__deleted=False,deleted=False).order_by('-id')
    paginator = Paginator(store_list,5)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        stores = paginator.page(page)
    except:
        stores = paginator.page(paginator.num_pages)
    return direct_to_template(request,'store/search_base.html',{'paginator':paginator,'new_stores':new_stores,'new_arrival':new_arrival,'page_obj':stores,'form':form,'form2':form2,'flag':flag,'temp_flg':flg,'code_flg':code_flg,'gets_string':get_string})

@login_required
def item_add(request,line_id):
    i=0
    data = []
    line = Line.objects.get(pk=line_id,store__deleted=False)
    try:
        store_date = Store.objects.get(user=request.user,id=line.store.id,deleted=False)
    except:
        raise Http404
    store_id = line.store.id
    lines = Line.objects.filter(store=store_id,store__deleted=False).order_by('-id')
    msg = ''
    for items in lines:
        data.append({'no':i,'id':items.id})
        i +=1
    for temp in data:
        if temp['id']==int(line_id):
            items=temp['no']
    if request.method == "POST":
        if request.POST.get('save'):
            form = ItemForm(data=request.POST,files=request.FILES)
            if form.is_valid():
                new_item=form.save(commit=False)
                new_item.line=line
                store_date.last_updated =datetime.now()
                store_date.save()
                new_item.save()
                item_id=new_item.id
                newest_item = Item.objects.get(id=item_id,deleted=False)
                fans = Addicted.objects.filter(store=store_date,deleted=False)
                subject = str(store_date.name)+" has add item"+newest_item.item+" at "+store_date.last_updated.strftime('%Y-%b-%d')
                message = "Hello Fashion Fans "+store_date.name+" has add item"+newest_item.item+" category : " +newest_item.line.category.name+" at "+store_date.last_updated.strftime('%Y-%b-%d')+". See the changes of the store by log in into your fashion account. Regards, Fashion Teams"
                for fan in fans:
                        msg=Message.objects.create(subject=subject,message=message,files=None)
                        MessageList.objects.create(thread=msg,reply=None,from_user=store_date.user,to_user=fan.user,message_type=4)
                return HttpResponseRedirect(reverse('add_item_complete',args=(item_id,)))
        else:
            form = ItemForm(data=request.POST,files=request.FILES)
            if form.is_valid():
                new_item=form.save(commit=False)
                new_item.line=line
                store_date.last_updated =datetime.now()
                store_date.save()
                new_item.save()
                return HttpResponseRedirect(reverse('item_add',args=(line.id,)))
    else:
        form = ItemForm()
    return direct_to_template(request,'clothing/add_item.html',
                                    {
                                         'form':form,
                                    })

def add_item_complete(request,item_id):
    i=0
    data=[]
    item = Item.objects.get(pk=item_id,deleted=False)
    store_id= item.line.store.id
    lines= Line.objects.filter(store=store_id).order_by('-id')
    for items in lines:
        data.append({'no':i,'id':items.id})
        i +=1
    for temp in data:
        if temp['id']==int(item.line.id):
            items=temp['no']
    return direct_to_template(request,'clothing/add_item_complete.html',
                                    {
                                         'item':item,
                                    })

def view_item(request,line_id):
    i=0
    data = []
    owner_flag=0 # default flag for the user who login isnt the owner
    cache_time = 1800 # default cache time if the user who login isnt the owner
    line= get_object_or_404(Line,pk=line_id)
    item = Item.objects.filter(line=line.id,deleted=False,line__store__deleted=False).order_by('-set_primary_date','-id')
    lines= Line.objects.filter(store=line.store,store__deleted=False).order_by('-id')
    paginator = Paginator(item,30)
    page_num = int(request.GET.get('page',1))
    if request.user.id == line.store.user.id:
        owner_flag = 1
        cache_time = 60
    else:
        owner_flag = 0
    
    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return direct_to_template(request,'clothing/view_item.html',
                                {
                                       'line':line,
                                       'paginator':paginator, #name must be 'paginator' to use google paginator
                                       'page_obj': page, #name must be 'page_obj' to use google paginator
                                       'owner_flag':owner_flag,
                                       'page_num':page_num,
                                       'cache_time':cache_time,
                                })

def view_same_collection(request,line_name):
    i=0
    data = []
    if not line_name:
        raise Http404
    lines= Line.objects.filter(slug=line_name)
    for line in lines:
        line.my_items = line.item_set.filter(deleted=False).order_by('-set_primary_date','-id')
    paginator = Paginator(lines,7)
    page_num = int(request.GET.get('page',1))
    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return direct_to_template(request,'store/view_same_collection_name.html',
                                {
                                       'flag_line':lines[0],
                                       'paginator':paginator, #name must be 'paginator' to use google paginator
                                       'page_obj': page
                                })
@login_required
def edit_item(request,line_id):
    i=0
    data=[]
    try:
        item= Item.objects.get(pk=line_id,deleted=False,line__store__deleted=False)
    except:
        raise Http404
    store_id = item.line.store.id
    lines= Line.objects.filter(store=store_id,store__deleted=False).order_by('-id')
    for items in lines:
        data.append({'no':i,'id':items.id})
        i +=1
    for temp in data:
        if temp['id']==int(item.line.id):
            items=temp['no']
    if request.method=="POST":
        edititemform = EditItemForm(data=request.POST,files=request.FILES,instance=item)
        if edititemform.is_valid():
            item.last_updated = datetime.now()
            item.save()
            edititemform.save()
            return HttpResponseRedirect(reverse('detail_items',args=(item.id,slugify(item.item))))
    else:
        edititemform = EditItemForm(instance=item)
    return direct_to_template(request,'clothing/edit_item.html',
                                {
                                      'edititemform': edititemform,
                                      'item':item,
                                })
@login_required
def remove_item(request,item_id):
    user = get_object_or_404(User,pk=request.user.id)
    store = Store.objects.get(user=user,deleted=False)
    try:
        remove = Item.objects.get(id=item_id,line__store=store,deleted=False)
    except:
        raise Http404
    remove.deleted = True
    remove.save()
    return HttpResponseRedirect(reverse('view_line',args=(store.id,)))

@login_required
def remove_item2(request,item_id):
    user = get_object_or_404(User,pk=request.user.id)
    try:
        store = Store.objects.get(user=user,deleted=False)
        remove = Item.objects.get(id=item_id,line__store=store,deleted=False)
    except:
        raise Http404
    remove.deleted = True
    remove.save()
    return HttpResponseRedirect(reverse('view_item',args=(store.id,)))

def redir_detail_item(request,item_id):
    item_slug = get_object_or_404(Item,pk=item_id,deleted=False,line__store__deleted=False).slug
    return HttpResponsePermanentRedirect(reverse('item_info',args=(item_id,item_slug,)))

def detail_items(request,item_id,item_slug):
    rate_date = None
    flag =0
    target=[] # list of email to store all email of people
              #that already comment this item( just like facebook comment,
              #if there is new comment in this item all of the others would get notification
    item = get_object_or_404(Item,pk=item_id,line__store__deleted=False,deleted=False)
    category = item.line.category
    store_id= item.line.store.id
    related_items = Item.objects.filter(line__category = category, line__store__deleted=False,deleted=False)
    related_items = random.sample(related_items,related_items.count())
    lines= Line.objects.filter(store=store_id).order_by('-id')

    formcomment =  CommentForm(data=request.POST)
    try:
        addict = Addicted.objects.get(user=request.user,store=store_id,deleted=False)

    except:
        addict = None
    try:
        rate_date = RatingCounter.objects.get(user=request.user,pub_date=date.today(),item=item_id)

        if rate_date:
            flag = 1
    except:
        rate_date = None
        flag =0

    try:
        compare_list = Compare_List.objects.get(user=request.user.id,item=item)
    except:
        compare_list= None
    store_owner = item.line.store.user
    if store_owner != request.user:
        try:
            view = View.objects.get(item=item,item__deleted=False)
            view.count = view.count+1
            view.save()
        except:
            View.objects.create(item=item,count=1)
    if request.method=="POST":
        if formcomment.is_valid():
            www="http://www.fashionment.com"+reverse('detail_items',args=(item_id,item_slug))
            subject = "User "+request.user.username+" has sent you comment your item "
            message = "User "+request.user.username+" has sent you message about "+item.item+" item. Read further information by log in into your fashion account and go to this url "+www+"."
            msg_to_mail="User "+request.user.username+" has sent you message about "+item.item+" item. \n Read further information by log in into your fashion account and go to this url "+www+". \n Regards , \n Fashion Team. "
            new_msg=Message.objects.create(subject=subject,message=message)
            comment_save=formcomment.save(commit=False)
            comment_save.user_id=request.user.id
            comment_save.store_id=None
            comment_save.item_id=item.id
            comment_save.date_added = datetime.now()
            comment_save.save()
            try:
                comment_plus = CommentNumber.objects.get(item=item.id)
                comment_plus.count = comment_plus.count+1
                comment_plus.save()
            except:
                CommentNumber.objects.create(item=item,count=1)

            if store_owner.id != request.user.id:
                user= User.objects.get(id=request.user.id)
                MessageList.objects.create(thread=new_msg,reply=None,from_user=user,to_user=store_owner,message_type=4,notification_type=2)
                email = EmailMessage(
                                 subject=subject,
                                 body=msg_to_mail,
                                 from_email=request.user.email,
                                 to=[store_owner.email],
                                )
            else:
                item_comment = Comment.objects.filter(item=item).exclude(user__id=request.user.id)
                for target_user in item_comment:
                    to_user = User.objects.get(id=target_user.user.id)
                    MessageList.objects.create(thread=new_msg,reply=None,from_user=store_owner,to_user=target_user.user,message_type=4,notification_type=2)
                    if target:
                        for temporary in target:
                            if not temporary in target:
                                target.append(to_user.email)
                    else:
                        target.append(to_user.email)
                email = EmailMessage(
                                 subject=subject,
                                 body=msg_to_mail,
                                 from_email=request.user.email,
                                 to=target,
                                )
            email.send()
            request.user.message_set.create(message="Please wait for few minutes before we upload your comment.")
            return HttpResponseRedirect(reverse('detail_items',args=(item_id,item_slug,)))
    if request.user.id==item.line.store.user.id:
        flag=1
    if not request.user.id:
        flag=1
    return direct_to_template(request,'clothing/detail_items.html',{
                                'item':item,
                                'form':formcomment,
                                'compare_list':compare_list,
                                'flag':flag,
                                'addict':addict,
                                'related_items':related_items,
                                'prev':item.get_previous_item(),
                                'next':item.get_next_item(),
                                'lines':lines,
                            })

@login_required
def line_add(request):
    try:
        store = Store.objects.get(user=request.user.id, deleted=False)
    except:
        raise Http404
    if request.method == "POST":
        form = LineForm(request.POST)
        if form.is_valid():
            add_line=form.save(commit=False)
            add_line.store=store
            add_line.save()
            return HttpResponseRedirect(reverse('item_add',args=(add_line.id,)))
    else:
        form = LineForm()
    return direct_to_template(request,'store/add_line.html',
                                    {
                                         'add_line':form,
                                    })
                                    
@login_required
def edit_line(request,line_id):
    try:
        line = Line.objects.get(pk=line_id,store__deleted=False)
    except:
        raise Http404
    line_name = line.line
    store = line.store.slug
    if request.method =="POST":
        edit_line_form = EditLineForm(data=request.POST,instance=line)
        if edit_line_form.is_valid():
            edit_line_form.save()
            return HttpResponseRedirect(reverse('view_stores',args=(store,)))
    else:
        edit_line_form = EditLineForm(instance=line)
    return direct_to_template(request,'store/edit_line.html',
                                    {
                                        'edit_line_form':edit_line_form,
                                        'line_name':line_name,
                                    })

def view_line(request,store_id):
    lines = Line.objects.filter(store=store_id,store__deleted=False).order_by('-id')
    if not lines:
        raise Http404
    for line in lines:
        line.my_items = line.item_set.filter(deleted=False).order_by('-set_primary_date','-id')
    paginator = Paginator(lines,7)
    page_num = int(request.GET.get('page',1))
    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return direct_to_template(request,'store/view_line.html',{
                    'flag_line':lines[0],
                    'paginator':paginator, #name must be 'paginator' to use google paginator
                    'page_obj': page #name must be 'page_obj' to use google paginator
                })

@login_required
def addicted(request,user_id=None):
    if user_id:
        active_user = get_object_or_404(User,pk=request.user.id)
        try:
            store = Store.objects.get(user=user_id, deleted=False)
        except:
            raise Http404
        try:
            update=Addicted.objects.get(user=request.user.id,store=store.id)
        except:
            update=None
        if update:
            update.deleted=False
            update.save()
        else:
            if active_user.id != store.user_id:
                add_addict = Addicted.objects.create(user=active_user, store=store)

        return HttpResponseRedirect(reverse('view_stores',args=(store.slug,)))
    else:
        raise 404

def view_my_addict(request,store_id):
    addict = Addicted.objects.filter(store=store_id,deleted=False)
    return direct_to_template(request,'store/my_addicts.html',
                                {
                                    'my_addict':addict,
                                })

def addicts_to(request):
    addicts_to = Addicted.objects.filter(user=request.user.id,deleted=False)
    return direct_to_template(request,'store/addicts_to.html',
                                {
                                    'addicts_to':addicts_to,
                                })

@login_required
def remove_addict(request,addict_id):
    try:
        remove = Addicted.objects.get(user=request.user.id,id=addict_id)
    except:
        raise Http404
    remove.deleted = True
    remove.save()
    return HttpResponseRedirect(reverse('addicts_to'))

@login_required
def add_compare_item(request,item_id):
    user_active = get_object_or_404(User,pk = request.user.id)
    item = get_object_or_404(Item,pk=item_id)
    try:
        compare_list = Compare_List.objects.get(user=request.user.id,item=item)
    except:
        compare_list= None
    if compare_list:
        compare_list.deleted=False
        compare_list.save()
        return HttpResponseRedirect(reverse('detail_items',args=(item_id,slugify(item.item))))
    else:
        add_compare_list = Compare_List.objects.create(user=user_active,item=item)
    return HttpResponseRedirect(reverse('detail_items',args=(item.id,slugify(item.item))))

@login_required
def view_compare_list(request):
    user = get_object_or_404(User,pk=request.user.id)
    item_compare = Compare_List.objects.filter(user=user,deleted=False,item__line__store__deleted=False)
    count=0
    rating = None
    try:
        for item in item_compare:
            count+=1
    except:
        count=0
        rating = None
    paginator = Paginator(item_compare,11)
    page_num = int(request.GET.get('page',1))
    try:
        #contacts renamed to page (why was it named contacts anyway??)
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
        page_num = 1
    return direct_to_template(request,'clothing/view_compare_list.html',
                                {
                                    'item':item_compare,
                                    'paginator':paginator, #name must be 'paginator' to use google paginator
                                    'page_obj': page, #name must be 'page_obj' to use google paginator
                                    'rating':rating,
                                    'count':count,
                                    'page_num':page_num,
                                })
                                
@login_required
def remove_compare_list(request):
    if request.POST:
        for remove_list in request.POST.getlist('check'):
            compare_list_remove = Compare_List.objects.get(item=remove_list,user=request.user)
            compare_list_remove.deleted = True
            compare_list_remove.save()
        return HttpResponseRedirect(reverse('view_compare_list'))
    else:
        return HttpResponseRedirect(reverse('view_compare_list'))

@login_required
def view_compare_thumbnails(request):
    user = get_object_or_404(User,pk=request.user.id)

    item_compare = Compare_List.objects.filter(user=user,deleted=False,item__line__store__deleted=False,item__deleted=False)
    item = Item.objects.filter(item = item_compare,deleted=False,line__store__deleted=False)
    try:
        rating = Rating.objects.filter(item=item_compare)
    except:
        rating =None
    paginator = Paginator(item_compare,5)
    page_num = int(request.GET.get('page',1))
    try:
        #contacts renamed to page (why was it named contacts anyway??)
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
        page_num = 1
    return direct_to_template(request,'clothing/view_compare_thumbnails.html',
                                {
                                    'item':item_compare,
                                    'rating':rating,
                                    'paginator':paginator, #name must be 'paginator' to use google paginator
                                    'page_obj': page, #name must be 'page_obj' to use google paginator
                                    'page_num':page_num
                                })
@login_required
def remove_compare_thumbnails(request):
    if request.POST:
        for remove_list in request.POST.getlist('check'):
            compare_list_remove = Compare_List.objects.get(item=int(remove_list),user=request.user)
            compare_list_remove.deleted = True
            compare_list_remove.save()
        return HttpResponseRedirect(reverse('view_compare_thumbnails'))
    else:
        return HttpResponseRedirect(reverse('view_compare_thumbnails'))

@login_required
def view_detail_compare(request):
    item_data = None
    count=1
    if request.POST:

        for tick in request.POST.getlist('check'):
            count +=1
        if count == 2:
            return HttpResponseRedirect(reverse('view_compare_thumbnails'))
        else:
            item_data = Item.objects.filter(id__in=request.POST.getlist('check'))

    else:
        return HttpResponseRedirect(reverse('view_compare_thumbnails'))
    return direct_to_template(request,'clothing/view_detail_compare.html',
                                {
                                    'item':item_data,
                                    'count':count,
                                })

@login_required
def view_detail_compares(request):
    item_data = None
    count=1
    if request.POST:
        for tick in request.POST.getlist('check'):
            count +=1
        if count == 2:

            return HttpResponseRedirect(reverse('view_compare_list'))
        else:
            item_data = Item.objects.filter(id__in=request.POST.getlist('check'))
    else:
        return HttpResponseRedirect(reverse('view_compare_list'))
    return direct_to_template(request,'clothing/view_detail_compare.html',
                                {
                                    'item':item_data,
                                    'count':count,
                                })

def view_most_all(request,choose_slug,slug,type=None):
    stores=None
    items=None
    title = None
    msg = None
    err_msg = None
    page = 1
    if choose_slug=="store":
        if slug=="last-updated":
            title = "Last Updated"
            msg = "updated"
            try:
                stores = Store.objects.filter(deleted=False).order_by('-last_updated')
                if type=='store':
                    stores = stores.filter(user__account_type=1)
                elif type=='designer':
                    stores = stores.filter(user__account_type=2)
                else:
                    raise Http404
            except:
                stores = None
                items = None
        elif slug=="most-viewed":
            title = "Most Viewed"
            msg = "viewed"
            try:
                stores = View.objects.filter(store__deleted=False).order_by('-count')
                if type=='store':
                    stores = stores.filter(store__user__account_type=1)
                elif type=='designer':
                    stores = stores.filter(store__user__account_type=2)
                else:
                    raise Http404
            except:
                stores = None
        elif slug == "most-commented" :
            title = "Most Commented"
            msg = "commented"
            try:
                stores = CommentNumber.objects.filter(store__deleted=False).order_by('-count')
                if type=='store':
                    stores = stores.filter(store__user__account_type=1)
                elif type=='designer':
                    stores = stores.filter(store__user__account_type=2)
                else:
                    raise Http404
            except:
                stores = None
        elif slug == "most-favourite" :
            title = "Most Favourited"
            try:
                stores = Rating.objects.filter(store__deleted=False).order_by('-avg_rate')
                if type=='store':
                    stores = stores.filter(store__user__account_type=1)
                elif type=='designer':
                    stores = stores.filter(store__user__account_type=2)
                else:
                    raise Http404
            except:
                stores = None

    if choose_slug=="items":
        if slug=="last-updated":
            title = "Last Updated"
            msg = "updated"
            try:
                items = Item.objects.filter(deleted=False).order_by('-last_updated')
            except:
                items = None
        elif slug=="most-viewed":
            title = "Most Viewed"
            msg = "viewed"
            try:
                items = View.objects.filter(item__deleted=False,item__line__store__deleted=False).order_by('-count')
            except:
                items = None

        elif slug == "most-commented" :
            title = "Most Commented"
            msg = "commented"
            try:
                items = CommentNumber.objects.filter(item__deleted=False,item__line__store__deleted=False).order_by('-count')
            except:
                items = None
        elif slug == "most-favourite" :
            title = "Most Favourited"
            try:
                items = Rating.objects.filter(item__deleted=False,item__line__store__deleted=False).order_by('-avg_rate')
            except:
                items = None
    if stores:
        paginator = Paginator(stores,30)
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1
        try:
            stores_list = paginator.page(page)
        except:
            stores_list = paginator.page(paginator.num_pages)
    else:
        stores_list = stores
    if items:
        paginator2 = Paginator(items,30)
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1
        try:
            items_list = paginator2.page(page)
        except:
            items_list = paginator2.page(paginator2.num_pages)
    else:
        items_list=items
        
    return direct_to_template(request,'store/most.html',{'stores':stores_list,'slug':slug,'items':items_list,'title':title,'msg':msg,'err':err_msg,'type':type,'page_num':page})


def view_most_store(request,store_type,store_slug=None):
    stores=  title = msg =  stores2 = ctr_store = None
    
    total_ctr_store = 0
    
    store_click = 1
    if store_slug=="last-updated":
        title = "Last updated"
        msg = "has updated"
        store_click = 1
        try:
            all_store = Store.objects.filter(deleted=False).order_by('-last_updated')
            if store_type=="store":
                stores = all_store.filter(user__account_type=1)
            elif store_type=="designer":
                stores = all_store.filter(user__account_type=2)
            else:
                raise Http404
        except:
            stores = None
    elif store_slug=="most-viewed":
        title = "Most viewed"
        msg = "have been view"
        store_click = 2
        
        try:
            all_store = View.objects.filter(item__isnull=True,store__deleted=False).order_by('-count')
            if store_type=="store":
                stores = all_store.filter(store__user__account_type=1)
            elif store_type=="designer":
                stores = all_store.filter(store__user__account_type=2)
            else:
                raise Http404
        except:
            stores = None
    elif store_slug == "most-commented" :
        title = "Most comment"
        msg = "have been comment"
        store_click = 3
        
        all_store = CommentNumber.objects.filter(item__isnull=True,store__deleted=False).order_by('-count')
        if store_type=="store":
            stores = all_store.filter(store__user__account_type=1)
        elif store_type=="designer":
            stores = all_store.filter(store__user__account_type=2)
        else:
            raise Http404
            
    elif store_slug == "most-favourite" :
        title = "Most favourite"
        msg = "have been rate"
        store_click = 4
        try:
            all_store = Rating.objects.filter(item__isnull=True,store__deleted=False).order_by('-avg_rate')
            if store_type=="store":
                stores = all_store.filter(store__user__account_type=1)
            elif store_type=="designer":
                stores = all_store.filter(store__user__account_type=2)
            else:
                raise Http404
        except:
            stores = None

    
    if stores:
        if stores.count()<5:
             total_ctr_store = 5-stores.count()
    else:
        total_ctr_store = 5
    ctr_store = xrange(0,total_ctr_store)
    return direct_to_template(request,'store/mostform.html',{'stores':stores,'title':title,'msg':msg,'stores2':stores2,'ctr_store':ctr_store,'temp_flg':total_ctr_store,'click':store_click,'store_type':store_type})

def view_most_item(request,item_slug=None):
    total_ctr_item = items = title = msg = err_msg = invitation_msg = ctr_item = total_ctr_item = None
    item_click=1
    data = []
    temporary_stored_item=[]
    newly_store = []
    from_user = request.user
    form =""
    if item_slug=="last-updated":
        title = "Last updated"
        msg = "has updated"
        item_click = 1
        ###### function below to make sure only 1 item for each store that would be shown at index mostly things
        try:
            items = Item.objects.filter(line__store__deleted=False,deleted=False).order_by('-last_updated')
            for item in items:
                if not newly_store:
                    newly_store.append(item.line.store.id)
                    temporary_stored_item.append(item.id)
                else:
                    if not item.line.store.id in newly_store:
                        newly_store.append(item.line.store.id)
                        temporary_stored_item.append(item.id)
            items = items.filter(id__in=temporary_stored_item)
        except:
            items = None

    elif item_slug=="most-viewed":
        title = "Most viewed"
        msg = "have been view"
        try:
            items = View.objects.filter(store__isnull=True,item__line__store__deleted=False,item__deleted=False).order_by('-count')
        except:
            items = None
        item_click = 2
    elif item_slug == "most-commented" :
        title = "Most comment"
        msg = "have been comment"
        try:
            items = CommentNumber.objects.filter(store__isnull=True,item__line__store__deleted=False,item__deleted=False).order_by('-count')
        except:
            items = None
        item_click = 3
    elif item_slug == "most-favourite" :
        title = "Most favourite"
        msg = "have been rate"
        try:
            items = Rating.objects.filter(store__isnull=True,item__line__store__deleted=False,item__deleted=False).order_by('-avg_rate')
            
        except:
            items = None
        item_click = 4
    elif item_slug == "invite-friend":
        title = "Invitation"
        msg = None
        item_click = 5
        if request.user.id:
            try:
                from_user = Store.objects.get(user=request.user)
            except:
                from_user = User.objects.get(id = request.user.id)
            if request.POST :
                form = InviteForm(request.POST)
                if request.user.id:
                    if form.is_valid():
                        data.append(request.POST.get('email'))
                        for i in xrange(2,10):
                            data.append(request.POST.get('email'+str(i)))
                        www = "http://www.fashionment.com"
                        msg=str(request.user)+" has invited you to join "+ www +". Below is his/her personal message:\n "
                        email = EmailMessage(
                                     subject='Invitation to Fashionment',
                                     body=msg+'"'+request.POST.get('message')+'"'+" \n \n Thank you and see you online soon at Fashionment! \n\n Regards,\nFashionment Team",
                                     from_email=request.user.email,
                                     to=data,
                                    )
                        email.send()
                        store_slug = "invite-complete"
                        return HttpResponseRedirect(reverse('view_most_store',args=(item_slug,)))
            else:
                form = InviteForm()
        else:
            return HttpResponseRedirect(reverse('auth_login'))
    elif item_slug == "invite-complete" :
        title = "Invitation"
        invitation_msg = "invite"
        item_click = 5
    #raise Exception(form)
    if items :
        if items.count()<5:
            total_ctr_item = 5-items.count()
            ctr_item = xrange(0,total_ctr_item)
    else:
        total_ctr_item = 5
        ctr_item = xrange(0,total_ctr_item)
    return direct_to_template(request,'store/mostformitem.html',{'items':items,'title':title,'msg':msg,'err':err_msg,'from':from_user,'form':form,'invitecomplete':invitation_msg,'ctr_item':ctr_item,'temp_flg':total_ctr_item,'click':item_click})

#@cache_page(5)
def view_home(request):
    front_news = FashionFacts.objects.filter(status="1").order_by('-pub_date')
    #voucherform = VoucherForm()
    loop = 0
    all_horoscope = Horoscope.objects.all()
    big_horoscope = all_horoscope.filter(show=True)
    if all_horoscope:
        loop = 0
        for horoscope in all_horoscope:
            if loop%4==0:
                horoscope.new_col = True
            loop+=1
    store_link = "/fashion/store/most/store/most-viewed/"
    designer_link = "/fashion/store/most/designer/most-viewed/"
    store_promotion = Store.objects.filter(deleted=False,promotion_text__isnull=False).exclude(promotion_text='').order_by('-last_updated')
    item_link = "/fashion/items/most-viewed/"
    object=[]
    array = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0-9']
    divide = 5
    div_id=0
    type="store"
    loop = 1
    for char in array:
        from django.db.models import Q
        args = Q()
        temporary = Store.objects.filter(args)
        if char!="0-9":
            temporary = Store.objects.filter(deleted=False,name__istartswith=str(char),user__account_type=1).order_by('name')
        else:
            for i in xrange(0,10):
                args = args|Q(deleted=False,name__startswith=i)
            temporary = temporary.filter(args)
        if char=="0-9":
            link_back=True
        elif loop %15==0:
            if loop != 0:
                link_back=True
                div_id+=1
            else:
                link_back=False
                
        else:
            link_back=False
        if loop % divide ==0:
            if loop != 0:
                clear=True
            else:
                clear=False
        else:
            clear = False
        loop+=1
        object.append({'alphabet':char,'object':temporary,'clear':clear,'link_back':link_back,'div_id':div_id})
    return direct_to_template(request,'index.html',{'store_link':store_link,'designer_link':designer_link,'front_news':front_news,'store_promotion':store_promotion,'item_link':item_link,'all_horoscope':all_horoscope,'big_horoscope':big_horoscope,'array':array,'type':type,'object':object})


@login_required
def primary_picture(request,line_id):
    primary_pictures=''
    if request.POST:
        primary_pictures = Item.objects.filter(line=line_id,deleted=False)
        for picture_set in primary_pictures:
            set_primary_pictures = Item.objects.get(id=picture_set.id)
            set_primary_pictures.primary=False
            set_primary_pictures.set_primary_date=None
            set_primary_pictures.save()

        for picture_set1 in request.POST.getlist('check'):
            #return HttpResponse(request.POST.getlist('check'))
            set_primary_pictures = Item.objects.get(id=picture_set1,deleted=False)
            set_primary_pictures.primary=True
            set_primary_pictures.set_primary_date=datetime.now()
            set_primary_pictures.save()
        return HttpResponseRedirect(reverse('view_item',args=(line_id,)))
    else:
        primary_pictures1 = Item.objects.filter(line=line_id,deleted=False)
        for picture_set in primary_pictures1:
            set_primary_pictures = Item.objects.get(id=picture_set.id)
            set_primary_pictures.primary=False
            set_primary_pictures.set_primary_date=None
            set_primary_pictures.save()

        return HttpResponseRedirect(reverse('view_item',args=(line_id,)))


@login_required
def rate_store(request,store_id):
    temp_rate=0
    update=None
    if request.POST:
        active_user = User.objects.get(pk=request.user.id)
        store = Store.objects.get(id=store_id,deleted=False)
        for rate in request.POST.getlist('star'):
            RatingCounter.objects.create(user=active_user,store=store,rate=rate,pub_date=date.today())
        try:
            update=Rating.objects.get(store=store)
            rate_ctr = RatingCounter.objects.filter(store=store)
            for rate in rate_ctr :
                temp_rate +=rate.rate
            temp_rate = temp_rate/rate_ctr.count()
            update.avg_rate = temp_rate
            update.save()
        except:
            for rate in request.POST.getlist('star'):
                Rating.objects.create(store=store,avg_rate=rate)

        return HttpResponseRedirect(reverse('notice_store',args=(store_id,)))


def store_notice(request,store_id):
    store = Store.objects.get(id=store_id)
    return direct_to_template(request,'result3.html',{'store':store})

@login_required
def rate_item(request,item_id):
    temp_rate=0
    update=None
    if request.POST:
        active_user = get_object_or_404(User,pk=request.user.id)
        try:
            item = Item.objects.get(id=item_id,deleted=False)
        except:
            raise Http404
        for rate in request.POST.getlist('star'):
            RatingCounter.objects.create(user=active_user,item=item,rate=rate,pub_date=date.today())
        try:
            update=Rating.objects.get(item=item)
            rate_ctr = RatingCounter.objects.filter(item=item)
            for rate in rate_ctr :
                temp_rate +=rate.rate
            temp_rate = temp_rate/rate_ctr.count()
            update.avg_rate = temp_rate
            update.save()
        except:
            for rate in request.POST.getlist('star'):
                Rating.objects.create(item=item,avg_rate=rate)


        return HttpResponseRedirect(reverse('notice_item',args=(item_id,)))

def item_notice(request,item_id):
    item = get_object_or_404(Item,id=item_id)

    return direct_to_template(request,'result4.html',{'item':item})


@login_required
def message_fashion_owner(request,item_id):
    item = get_object_or_404(Item,id=item_id)
    to_user = item.line.store.user
    to_user2 = get_object_or_404(User,id=to_user.id)
    from_user = get_object_or_404(User,id=request.user.id)
    form = MessageToUser()
    position = 0
    if request.POST:
        form = MessageToUser(request.POST)
        if form.is_valid():
            www="http://www.fashionment.com"+reverse('inbox',args=('',))
            form.save(commit=False)
            new_msg=form.save()
            MessageList.objects.create(thread=new_msg,reply=None,from_user=from_user,to_user=to_user2,message_type=request.POST.get('message_type'))
            subject = "User "+request.user.username+" has sent you message in fashion"
            message = "User "+request.user.username+" has sent you message about "+item.item+" item. Read further information by log in into your fashion account and go to this url"+www+". \n Regards , \n Fashion Team. "
            email = EmailMessage(
                                 subject=subject,
                                 body=message,
                                 from_email="mailer@empiria.com",
                                 to=[to_user2.email],
                                )
            email.send()
            return HttpResponseRedirect(reverse('message_complete'))
    else:
        temp = "Fashion "+ item.item + " item , ID : "+str(item.id)
    return direct_to_template(request,'mail/contact.html',{'form':form,'position':position,'temp':temp})

@login_required
def remove(request,slug,item_id=None):
    user = get_object_or_404(User,pk=request.user.id)
    store = Store.objects.get(user=user,deleted=False)
    lines = Line.objects.filter(store=store,store__deleted=False).order_by('-id')
    item=''
    if slug=="line":
        if item_id:
            raise Http404
        if lines:
            for line in lines:
                line.my_items = line.item_set.filter(deleted=False).order_by('-set_primary_date','-id')
    elif slug=="item":
        if item_id:
            item = get_object_or_404(Item,id=item_id,deleted=False)
        else:
            raise Http404
    paginator = Paginator(lines,7)
    page_num = int(request.GET.get('page',1))
    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    return direct_to_template(request,'store/remove_item_or_line.html',{'store':store,
                    'item':item,
                    'paginator':paginator, #name must be 'paginator' to use google paginator
                    'page_obj': page})

@login_required
def remove_line(request):
    user = get_object_or_404(User,pk=request.user.id)
    store = get_object_or_404(Store,user=user,deleted=False)
    thicked = request.POST.getlist('line_checked')
    items=''
    if thicked:
        lines = Line.objects.filter(id__in=thicked,store=store,store__deleted=False).order_by('-id')
    else:
        lines = ''
    if lines :
        for line in lines:
                line.my_items = line.item_set.filter(deleted=False).order_by('-set_primary_date','-id')
    paginator = Paginator(lines,7)
    page_num = int(request.GET.get('page',1))
    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return direct_to_template(request,'store/view_remove.html',{'page_obj':page,'paginator':paginator,'item':items,'view_line':lines,})

@login_required
def delete_line(request):
    thicked = request.POST.getlist('line_checked')
    if thicked:
        lines = Line.objects.filter(pk__in = thicked)
        for line in lines:
            all_item = Item.objects.filter(line=line)
            all_item.delete()
        lines.delete()
    return HttpResponseRedirect(reverse('view_store'))

@login_required
def remove_picture(request,item_id):
    user = get_object_or_404(User,id=request.user.id)
    store = get_object_or_404(Store,user=user)
    item=get_object_or_404(Item,line__store=store,deleted=False,id=item_id)
    item.picture2=''
    item.save()
    return HttpResponseRedirect(reverse('edit_item',args=(item_id,)))

@login_required
def remove_comment(request,comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.item:
        slug="item"
        id = comment.item.id
    else:
        slug = "store"
        id = comment.store.id
    comment.delete()
    return HttpResponseRedirect(reverse('view_comment',args=(slug,id,)))

@login_required
def delete_item(request,item_id):
    user = get_object_or_404(User,pk=request.user.id)
    try:
        store = Store.objects.get(user=user,deleted=False)
        remove = Item.objects.get(id=item_id,line__store=store,deleted=False)
    except:
        raise Http404
    comment = Comment.objects.filter(item=remove)
    commentnumber = CommentNumber.objects.filter(item=remove)
    rating = Rating.objects.filter(item=remove)
    ratingcounter = RatingCounter.objects.filter(item=remove)
    view = View.objects.filter(item=remove)
    compare_list = Compare_List.objects.filter(item=remove)
    compare_list.delete()
    comment.delete()
    commentnumber.delete()
    rating.delete()
    ratingcounter.delete()
    view.delete()
    remove.delete()
    
    return HttpResponseRedirect(reverse('view_store'))

def view_detail_pic(request,item_id,slug):
    item = get_object_or_404(Item,id=item_id)
    image = ''
    if slug=="picture1":
        image = item.picture1
    if slug=="picture2":
        if item.picture2:
            image=item.picture2
    return direct_to_template(request,'clothing/view_detail_picture.html',{
                                    'item':item,
                                    'image':image,
                                    'slug':slug,
                                  })
@login_required
def report_content(request,id,slug):
    to_email = "customer-support@fashionment.com"
    previous_url=''
    if slug=="item":
        item = get_object_or_404(Item,id=id,deleted=False)
        previous_url = reverse('detail_items',args=(item.id,slugify(item.item)))
        report_location = "http://www.fashionment.com"+previous_url
        body = "User "+str(request.user)+" reporting "+str(item.item)+" item had an inappropriate content.\n To see the content by go to this url : "+report_location
    elif slug=="comment":
        comment = get_object_or_404(Comment,id=id)
        if comment.item:
            previous_url=reverse('detail_items',args=(comment.item.id,slugify(comment.item.item)))
        else:
            previous_url=reverse('view_store',args=(comment.store.id,))
        body = "User "+str(request.user)+" reporting comment that was created by "+str(comment.user)+" had an inappropriate content.\n To see the content by go to this url : "+report_location
    elif slug=="store":
        store = get_object_or_404(Store,id=id,deleted=False)
        previous_url = reverse('view_stores',args=(store.slug,))
        report_location = "http://www.fashionment.com"+previous_url
        body = "User "+str(request.user)+" reporting store name "+str(store.name)+" had an inappropriate content.\n To see the content by go to this url : "+report_location
    elif slug=="profile":
        profile = get_object_or_404(User,id=id)
        previous_url = reverse('view_profile',args=(profile.id,))
        report_location = "http://www.fashionment.com"+previous_url
        body = "User "+str(request.user)+" reporting user "+str(profile.username)+" had an inappropriate content.\n To see the content by go to this url : "+report_location
    else:
        raise 404
    subject = "Content an inappropriate  at "+report_location
    email = EmailMessage(
                             subject=subject,
                             body=body,
                             from_email=request.user.email,
                             to=[to_email],
                            )
    email.send()
    return HttpResponseRedirect(previous_url)

def view_all_designer(request,slug=None):
    designer = Store.objects.filter(user__account_type=2,deleted=False)
    object = []
    target=[]
    no_item = []
    if request.method=="POST":
        page_num = request.GET.get('page')
        designer_id = request.POST.get('designer_id')
        commented_designer = Store.objects.get(id=designer_id)
        formcomment=CommentForm(data=request.POST)
        if not request.user.id:
            return HttpResponseRedirect(reverse('auth_login'))
        if formcomment.is_valid():
            www="http://www.fashionment.com"+reverse('view_stores',args=(commented_designer.slug,))
            subject = "User "+str(request.user.username)+" has sent you a comment about your portfolio "
            message = "User "+str(request.user.username)+" has sent you a comment about "+str(commented_designer.name)+". Read further information by log in into your fashion account and go to this url  "+www+"."
            msg_to_mail="User "+str(request.user.username)+" has sent you message about "+str(commented_designer.name)+" portofolio. \n Read further information by log in into your fashion account and go to this url "+www+". \n Regards , \n Fashion Team. "
            new_msg=Message.objects.create(subject=subject,message=message)
            comment1=formcomment.save(commit=False)
            comment1.user_id=request.user.id
            comment1.store_id=designer_id
            comment1.item_id=None
            comment1.date_added=datetime.now()
            comment1.save()
            if commented_designer.user.id != request.user.id:
                user= User.objects.get(id=request.user.id)
                MessageList.objects.create(thread=new_msg,reply=None,from_user=user,to_user=commented_designer.user,message_type=4)
                email = EmailMessage(
                                 subject=subject,
                                 body=msg_to_mail,
                                 from_email=request.user.email,
                                 to=[commented_designer.user.email],
                                )
            else:
                store_comment = Comment.objects.filter(store=commented_designer).exclude(user__id=request.user.id)
                for target_user in store_comment:
                    to_user = User.objects.get(id=target_user.user.id)
                    MessageList.objects.create(thread=new_msg,reply=None,from_user=commented_designer.user,to_user=target_user.user,message_type=4)

                    if target:
                        for temporary in target:
                            if not temporary in target:
                                target.append(to_user.email)
                    else:
                        target.append(to_user.email)
                email = EmailMessage(
                                 subject=subject,
                                 body=msg_to_mail,
                                 from_email=request.user.email,
                                 to=target,
                                )
            email.send()
            try:
                comment_plus = CommentNumber.objects.get(store=commented_designer,store__deleted=False)
                comment_plus.count = comment_plus.count+1
                comment_plus.save()
            except:
                CommentNumber.objects.create(store=commented_designer,count=1)
            if not page_num:
                page_num = '1'
            request.user.message_set.create(message="Please wait for few minutes before we upload your comment.")
            return HttpResponseRedirect(reverse('view_all_designer',args=(slug,))+'?page='+str(page_num))
    else:
        formcomment = CommentForm()
    if slug=="most-viewed":
        designer = View.objects.filter(store__user__account_type=2,store__deleted=False).order_by('-count')
        title = "Most viewed"
    else:
        designer = designer.order_by('-last_updated')
        title="Last updated"
    for design in designer:
        no_item = []
        item = Item.objects.filter(line__store=design,deleted=False)
        for ctr in xrange(0,24-item.count()) :
          no_item.append(ctr)
        object.append({'designer':design,'items':item,'no_item':no_item})

    if object:
        paginator = Paginator(object,1)
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1
        try:
            object_list = paginator.page(page)
        except:
            object_list = paginator.page(paginator.num_pages)
    else:
        object_list = object
    return direct_to_template(request,'store/view_all_designer.html',{'object':object_list,'title':title,'form':formcomment,})

@login_required
def invite_friend(request):
    data = []
    if request.POST :
        form = InviteForm(request.POST)
        if request.user.id:
            if form.is_valid():
                data.append(request.POST.get('email'))
                for i in xrange(2,10):
                    data.append(request.POST.get('email'+str(i)))
                www = "http://www.fashionment.com"
                msg=str(request.user)+" has invited you to join "+ www +". Below is his/her personal message:\n "
                email = EmailMessage(
                             subject='Invitation to Fashionment',
                             body=msg+'"'+request.POST.get('message')+'"'+" \n \n Thank you and see you online soon at Fashionment! \n\n Regards,\nFashionment Team",
                             from_email=request.user.email,
                             to=data,
                            )
                email.send()
                title = "Invitation Complete"
                return direct_to_template(request,'store/invite_complete.html',{'title':title,})
    else:
        form = InviteForm()
    return direct_to_template(request,'store/invitation.html',{'form':form,})

@login_required
def confirm_remove_store(request):
    if request.user.id:
        store = get_object_or_404(Store,user__id=request.user.id,deleted=False)
    
    return direct_to_template(request,'store/remove_store_confirm.html',{'view_store':store,})

def indexing(request,type,alphabet=None):
    array = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0-9']
    object = []
    loop = 1
    divide = 5
    link_back=False
    div_id=0
    information_array= []
    
    array_list = []
    if request.is_ajax():
        if type!="collection":
            for char in array:
                url = reverse('indexing',args=(type,char,))
                information_array.append({'char':str(char).upper(),'url':url})
        else:
            array=LineCategory.objects.all()
            for character in array:
                url = ''
                array_list.append({'char':character.name,'url':url})
                
    if type=="store":
        object=[]
        if not alphabet:
            for char in array:
                if char!="0-9":
                    temporary = Store.objects.filter(deleted=False,name__istartswith=str(char),user__account_type=1).order_by('name')
                else:
                    from django.db.models import Q
                    args = Q()
                    temporary = Store.objects.filter(args)
                    for i in xrange(0,10):
                        args = args|Q(deleted=False,name__istartswith=i)
                    temporary = temporary.filter(args)
                if char=="0-9":
                    link_back=True
                elif loop %15==0:
                    link_back=True
                    div_id+=1
                else:
                    link_back=False
                if loop % divide ==0:
                    clear=True
                else:
                    clear = False

                loop+=1
                temporary = [dict(b) for b in temporary.values()]
                for store in temporary:
                    store['last_updated'] = store['last_updated'].strftime('%Y-%m-%d %H:%M')
                    if len(store['name'])>25:
                        store['name'] = store['name'][:25]+'...'
                    store['url']=reverse('view_stores',args=(store['slug'],))
                    store['name'] = capfirst(store['name'])
                char = capfirst(char)
                object.append({'alphabet':char,'object':temporary,'clear':clear,'link_back':link_back,'div_id':div_id})
            response_dict={
                    'array':information_array,
                    'type':type,
                    'object':object,
                    'alphabet':'',
                    }
        else:
            if alphabet=="0-9":
                from django.db.models import Q
                args = Q()
                temporary = Store.objects.filter(args)
                for i in xrange(0,10):
                    args = args|Q(deleted=False,name__istartswith=i,user__account_type=1)
                temporary = temporary.filter(args)
            else:
                temporary = Store.objects.filter(name__istartswith=alphabet,deleted=False,user__account_type=1).order_by('name')
            clear=False
            alphabet = alphabet.upper()
            temporary = [dict(b) for b in temporary.values()]
            for store in temporary:
                store['last_updated'] = store['last_updated'].strftime('%Y-%m-%d %H:%M')
                store['name'] = capfirst(store['name'])
                store['url']=reverse('view_stores',args=(store['slug'],))
            object.append({'alphabet':alphabet,'object':temporary,'clear':clear})
    elif type=="collection":
        object=[]
         # for ajax -> linecategory
        if not alphabet:
            array=LineCategory.objects.all()
            for character in array:
                temporary = Line.objects.filter(store__deleted=False,category__id=character.pk).select_related('category').order_by('line')
                temporary_line = temporary
                for temp_line in temporary_line:
                    show = False
                    same_name_filter = temporary.filter(line__istartswith=temp_line.line)
                    temp_line.same_name_count = same_name_filter.count()
                    if temp_line.same_name_count>1:
                        if temp_line.id==same_name_filter[0].id:
                            show = True
                    else:
                            show=True
                    temp_line.show=show
                if loop % divide == 0:
                    clear = True
                else:
                    clear = False
                loop+=1
                if request.is_ajax():
                    temporary_line=[dict(b) for b in temporary_line.values()]
                    for line in temporary_line:
                        show = False
                        same_name_filter = temporary.filter(line__istartswith=line['line'])
                        line['same_name_count'] = same_name_filter.count()
                        if line['same_name_count']>1:
                            if line['id']==same_name_filter[0].id:
                                show = True
                        else:
                                show=True
                        if line['same_name_count']==1:
                            line['url']=reverse('view_item',args=(line['id'],))
                        else:
                            line['url']=reverse('same_collection',args=(slugify(line['line']),))
                        if len(line['line'])>25:
                            line['line'] = line['line'][:25]+'...'
                        line['line'] = capfirst(line['line'])
                        line['show']=show
                    object.append({'alphabet':capfirst(character.name),'object':temporary_line,'clear':clear,'link_back':link_back,'div_id':div_id})
                else:
                    object.append({'alphabet':character,'object':temporary,'clear':clear,'link_back':link_back,'div_id':div_id})
            response_dict={
                    'array':array_list,
                    'type':type,
                    'object':object,
                    'alphabet':'',
                    }
        else:
            temporary = Line.objects.filter(category__name=alphabet,store__deleted=False).order_by('line')
            clear=False
            
            temporary_a = []
            for line in temporary :
                temporary_a.append({'alphabet':alphabet,'category_id':line.category.id,'category_name':line.category.name,'store':line.store.name,'slug':line.slug})
            object.append({'alphabet':alphabet,'object':temporary_a,'clear':clear,'link_back':link_back,'div_id':div_id})
    elif type=="designer":
        object=[]
        if not alphabet:
            for char in array:
                temporary = Store.objects.filter(deleted=False,name__istartswith=str(char),user__account_type=2).order_by('name')
                if char=="0-9":
                    link_back=True
                elif loop %15==0:
                    link_back=True
                    div_id+=1
                else:
                    link_back=False
                if loop % divide ==0:
                    clear=True
                else:
                    clear = False

                loop+=1
                temporary = [dict(b) for b in temporary.values()]
                for store in temporary:
                    store['last_updated'] = store['last_updated'].strftime('%Y-%m-%d %H:%M')
                    if len(store['name'])>25:
                        store['name'] = store['name'][:25]+'...'
                    store['name'] = capfirst(store['name'])
                    store['url']=reverse('view_stores',args=(store['slug'],))
                char = capfirst(char)
                object.append({'alphabet':char,'object':temporary,'clear':clear,'link_back':link_back,'div_id':div_id})
            response_dict={
                    'array':information_array,
                    'type':type,
                    'object':object,
                    'alphabet':'',
                    }
        else:
            if alphabet=="0-9":
                from django.db.models import Q
                args = Q()
                temporary = Store.objects.filter(args)
                for i in xrange(0,10):
                    args = args|Q(deleted=False,name__istartswith=i,user__account_type=2)
                temporary = temporary.filter(args)
            else:
                temporary = Store.objects.filter(name__istartswith=alphabet,deleted=False,user__account_type=2).order_by('name')
            clear=False
            alphabet = alphabet.upper()
            temporary = [dict(b) for b in temporary.values()]
            for store in temporary:
                store['last_updated'] = store['last_updated'].strftime('%Y-%m-%d %H:%M')
                store['name'] = capfirst(store['name'])
                store['url']=reverse('view_stores',args=(store['slug'],))
            object.append({'alphabet':alphabet,'object':temporary,'clear':clear})
    if alphabet:
        response_dict={
                    'array':information_array,
                    'type':type,
                    'object':temporary,
                    'alphabet':alphabet,
                    }
    if request.is_ajax():
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        return direct_to_template(request,'store/indexing.html',{'array':array,'type':type,'object':object})