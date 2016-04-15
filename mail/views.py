from mail.models import Message,MessageList,MessageForm,MessageToUser,ReplyMessage,SearchMessageForm,SearchNotificationForm
from accounts.models import User
from store.models import Store
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
#from products.models import Product
from datetime import datetime
from django.shortcuts import get_object_or_404

@login_required
def send_message(request,to_user=None):
    #return HttpResponse('|%s|%s|%s' % (to_user,message_id,product_id))
    subject=''
    position = 0
    ctr = True
    temp = ''
    exist_user = ''
    if to_user:
        target_user = User.objects.get(username=to_user)
    from_user = User.objects.get(pk=request.user.id)
    if request.POST:
        if to_user:
                form=MessageToUser(data=request.POST, files=request.FILES)
        else:
            form=MessageForm(request.POST, files=request.FILES)
        if form.is_valid():
            if to_user:
                form.save(commit=False)
                form.to_user = target_user
            else:
                to_user = request.POST.get('to_user')
                all_user = User.objects.all()
                for user in all_user:
                    full_name = user.first_name+" "+user.last_name
                    if full_name == to_user:
                        exist_user = user
                        to_user = user.id
                if not exist_user:
                    exist_user = Store.objects.get(name=to_user)
                    to_user = exist_user.user_id
                form.save(commit=False)
                target_user = User.objects.get(id=to_user)
            new_message = form.save()
            if request.POST.get('send'):

                    MessageList.objects.create(thread=new_message,reply=None,from_user=from_user,to_user=target_user,message_type=request.POST.get('message_type'),read=False)
                    subject = "User "+request.user.username+" had sent you message in fashion."
                    message=subject+" See futher information by log in into your fashion account."
                    from django.core.mail import EmailMessage
                    email = EmailMessage(
                                         subject=subject,
                                         body=message,
                                         from_email="mailer@empiria.com",
                                         to=[target_user.email],
                                        )
                    email.send()
                    return HttpResponseRedirect(reverse('message_complete'))
            else:

                    MessageList.objects.create(thread=new_message,reply=None,from_user=from_user,to_user=target_user,message_type=request.POST.get('message_type'),saved=True)
                    return HttpResponseRedirect(reverse('message_complete'))
    else:
        if to_user:
            form=MessageToUser()
        else:
            form = MessageForm()
        if request.GET:
            form.base_fields['subject'].initial = request.GET.get('subject')
    paginator = Paginator(temp,5)
    page_num = int(request.GET.get('page',1))
    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    return direct_to_template(request,'mail/contact.html',{'form':form,'position':position,'page_obj':page,'ctr':ctr})

@login_required
def inbox(request,message_id=None):
    flag = True # default true for inbox that doesnt had message_id( for different design in the same template)
    position=1 # 1 = inbox for search_mail content things
    messages = [] 
    user_active = get_object_or_404(User,pk=request.user.id)
    msg_subject = message_list = message_topic = from_user = page2 = None
    form = ReplyMessage()
    form2 = SearchMessageForm()
    msg_list = ''
    gets = {}
    get_string = ''
    search = request.GET.get('search')
    page_num = page = 1
    if message_id:
        flag = False
        mail = MessageList.objects.get(id=message_id,to_user = user_active,reply=None)
        msg = Message.objects.get(id=mail.thread.id)
        message_list = MessageList.objects.filter(thread=msg,inbox_deleted=False,notification_type__isnull=True).order_by('date_send')
        for messg in message_list:
            if messg.from_user != message_list[0].from_user and messg.reply:
                messages.append(messg)
            if messg.from_user == message_list[0].from_user :
                messages.append(messg)
        if mail.message_type == 1 :
               msg_type = 'Pricing'
        elif mail.message_type == 2:
               msg_type = 'Delivery'
        elif mail.message_type == 3:
               msg_type = 'Size&Colours'
        else :
               msg_type = 'Others'
        msg_subject = mail.thread.subject
        msg_subject = msg_type + ' - '+ msg_subject
        try:
               temp=MessageList.objects.get(thread=mail.thread,from_user=mail.to_user,to_user=mail.from_user,reply=None)
        except :
               temp=None
        if request.POST:
            form = ReplyMessage(data=request.POST, files=request.FILES)
            if form.is_valid():
                if request.POST.get('reply'):
                   form = ReplyMessage(request.POST,files=request.FILES).save(commit=False)
                   form.subject = 'RE: '+mail.thread.subject
                   form.save()
                   if temp==None :
                    MessageList.objects.create(thread=msg,reply=None,from_user=mail.to_user,to_user=mail.from_user,date_send=datetime.now())
                   MessageList.objects.create(thread=msg,reply=form,from_user=user_active,to_user=mail.from_user,date_send=datetime.now())

                   thread_owner = MessageList.objects.get(pk=mail.pk)
                   thread_owner.read = False
                   thread_owner.save()
                   subject = "User "+request.user.username+" had reply your message in fashion."
                   message=subject+" See futher information by log in into your fashion account."
                   from django.core.mail import EmailMessage
                   email = EmailMessage(
                                         subject=subject,
                                         body=message,
                                         from_email="mailer@empiria.com",
                                         to=[mail.from_user.email],
                                        )
                   email.send()
                   return HttpResponseRedirect(reverse('inbox',args=(message_id,)))
                if request.POST.get('delete'):
                    mail.inbox_deleted = True
                    mail.save()
                    return HttpResponseRedirect(reverse('inbox',args=('',)))
        mail.read = True
        mail.save()
        paginator = Paginator(messages,10)
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1
        try:
            msg_list = paginator.page(page)
            page2 = msg_list
        except(EmptyPage, InvalidPage):
            msg_list = paginator.page(paginator.num_pages)
            page2 = msg_list
    else:
        message_topic = MessageList.objects.filter(to_user=user_active,inbox_deleted=False,saved=False,reply=None,notification_type__isnull=True).order_by('-date_send')
        if request.POST :
            if not request.POST.get('searched'):
                for data in request.POST.getlist('topics'):
                    thread_change = MessageList.objects.get(pk=int(data))
                    if request.POST.get('unread'):
                        thread_change.read=False
                        thread_change.save()
                    if request.POST.get('read'):
                        thread_change.read=True
                        thread_change.save()
                    if request.POST.get('delete'):
                        thread_change.inbox_deleted=True
                        thread_change.save()
                    message_topic = MessageList.objects.filter(to_user=user_active,inbox_deleted=False,saved=False,reply=None,message_type=int(request.POST.get('select'))).order_by('-date_send')
            else:
                if request.POST.get('searched'):
                    search = request.POST.get('search')
                    message_topic = MessageList.objects.filter(to_user=user_active,inbox_deleted=False,reply=None,saved=False,from_user__username__contains=request.POST.get('search')).order_by('-date_send')
                    if not message_topic :
                        message_topic = MessageList.objects.filter(to_user=user_active,inbox_deleted=False,saved=False,reply=None,thread__subject__contains=request.POST.get('search')).order_by('-date_send')
                    if not message_topic:
                        message_topic = MessageList.objects.filter(to_user=user_active,inbox_deleted=False,saved=False,reply=None,thread__message__contains=request.POST.get('search')).order_by('-date_send')
        paginator = Paginator(message_topic,15)
        page_num = int(request.GET.get('page',1))
        try:
            page2 = paginator.page(page_num)
        except (EmptyPage, InvalidPage):
            page2 = paginator.page(paginator.num_pages)
    gets['search']= search
    get_string="&".join(["%s=%s" % (k, v) for k, v in gets.items()])
    try:
        from_user = message_list[0].from_user.username
    except:
        from_user=None
    return direct_to_template(request,'mail/inbox.html',{'page_obj':page2,'gets_string':get_string,'search':search,'message_list':msg_list,'from':from_user,'flag':flag,'form':form,'subject':msg_subject,'form2':form2,'position':position,'paginator':paginator,'topic_current_page':page_num,'msg_list_current_page':page,'msg_id':message_id})

@login_required
def send_items(request,message_id=None):
    form2 = SearchMessageForm()
    position=2
    page=''
    ctr = False
    paginator=''
    msg_list=''
    gets={}
    get_string=''
    search = request.GET.get('search')
    if message_id:
        flag = False
        message_list = MessageList.objects.filter(thread=message_id,from_user=request.user,reply__isnull=False,saved=False,send_deleted=False,notification_type__isnull=True)
        message_list2 = MessageList.objects.get(thread=message_id,from_user=request.user,reply__isnull=True,saved=False,send_deleted=False,notification_type__isnull=True)
        if message_list2 :
            subject = message_list2.thread.subject
            msg_type = message_list2.message_type
        else:
            subject = message_list[0].reply.subject
            msg_type = message_list2.message_type
        if msg_type == 1:
           msg_type = 'Pricing'
        elif msg_type==2:
               msg_type = 'Delivery'
        elif msg_type==3:
               msg_type = 'Size&Colours'
        else :
               msg_type = 'Others'
        msg_subject = subject
        msg_subject = msg_type + ' - '+ msg_subject
        msg_list = message_list
        if request.POST:
            for deleted in message_list:
                deleted.send_deleted = True
                deleted.save()
            message_list2.send_deleted = True
            message_list2.save()
            return HttpResponseRedirect(reverse('inbox2',args=('',)))
    else:
        subject = None
        flag = True
        message_list2 = None
        msg_subject = None
        message_list = MessageList.objects.filter(from_user=request.user,saved=False,send_deleted=False,reply__isnull=True,notification_type__isnull=True).order_by('-date_send')

        if request.POST :
            if not request.POST.get('searched'):
                for data in request.POST.getlist('topics'):
                    thread_change = MessageList.objects.get(pk=int(data))
                    if request.POST.get('delete'):
                        thread_change.send_deleted=True
                        thread_change.save()
                    else:
                        return HttpResponseRedirect(reverse('inbox2',args=('',)))
                try:
                    message_list = MessageList.objects.filter(from_user=request.user,saved=False,message_type=int(request.POST.get('select')),send_deleted=False,reply__isnull=True)
                except:
                    message_list = MessageList.objects.filter(from_user=request.user,saved=False,send_deleted=False,reply__isnull=True)
            if request.POST.get('searched'):
                message_list = MessageList.objects.filter(from_user=request.user,send_deleted=False,reply=None,saved=False,to_user__username__contains=request.POST.get('search')).order_by('-date_send')
                search = request.POST.get('search')
                
                if not message_list :
                    message_list = MessageList.objects.filter(from_user=request.user,send_deleted=False,saved=False,reply=None,thread__subject__contains=request.POST.get('search')).order_by('-date_send')
                if not message_list:
                    message_list = MessageList.objects.filter(from_user=request.user,send_deleted=False,saved=False,reply=None,thread__message__contains=request.POST.get('search')).order_by('-date_send')
            #elif request.POST.get
    paginator = Paginator(message_list,15)
    page_num = int(request.GET.get('page',1))
    gets['search']= search
    get_string="&".join(["%s=%s" % (k, v) for k, v in gets.items()])
    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
        
    return direct_to_template(request,'mail/send_items.html',{'page_obj':page,'search':search,'gets_string':get_string,'message_list2':message_list2,'subject':msg_subject,'flag':flag,'form2':form2,'message_topic':msg_list,'position':position,'paginator':paginator,'ctr':ctr,'msg_id':'message_id'})

@login_required
def draft(request,message_id=None):
    form2 = SearchMessageForm()
    position=3
    page = ''
    paginator=''
    ctr = False
    gets={}
    get_string=''
    search = request.GET.get('search')
    page = 1
    if message_id:
        flag = False
        try:
            message_list2 = MessageList.objects.get(thread=message_id,from_user=request.user,reply__isnull=True,saved=True,send_deleted=False,notification_type__isnull=True)
        except:
            raise Http404
        page = ''
        if message_list2 :
            subject = message_list2.thread.subject
            msg_type = message_list2.message_type
        if msg_type == 1:
           msg_type = 'Pricing'
        elif msg_type==2:
               msg_type = 'Delivery'
        elif msg_type==3:
               msg_type = 'Size&Colours'
        else :
               msg_type = 'Others'
        msg_subject = subject
        msg_subject = msg_type + ' - '+ msg_subject
        if request.POST:
            if request.POST.get('send'):
                message_list2.send_deleted = False
                message_list2.saved=False
                message_list2.save()
            if request.POST.get('delete'):
                message_list2.saved = False
                message_list2.inbox_deleted=True
                message_list2.send_deleted=True
                message_list2.save()
            return HttpResponseRedirect(reverse('inbox3',args=('',)))
    else:
        subject = None
        flag = True
        message_list2 = None
        msg_subject = None
        message_list = MessageList.objects.filter(from_user=request.user,saved=True,reply__isnull=True,send_deleted=False,notification_type__isnull=True).order_by('-date_send')
        if request.POST :
            if not request.POST.get('searched'):
                for data in request.POST.getlist('topics'):
                    thread_change = MessageList.objects.get(pk=int(data))
                    if request.POST.get('delete'):
                        thread_change.send_deleted=True
                        thread_change.save()
                    else:
                        return HttpResponseRedirect(reverse('inbox3',args=('',)))
                try:
                    message_list = MessageList.objects.filter(from_user=request.user,saved=True,message_type=int(request.POST.get('select')),reply__isnull=True,send_deleted=False).order_by('-date_send')
                except:
                    message_list = MessageList.objects.filter(from_user=request.user,saved=True,reply__isnull=True,send_deleted=False)
            if request.POST.get('searched'):
                    search = request.POST.get('search')
                    
                    message_list = MessageList.objects.filter(from_user=request.user,saved=True,reply=None,to_user__username__contains=request.POST.get('search')).order_by('-date_send')
                    if not message_list :
                        message_list = MessageList.objects.filter(from_user=request.user,saved=True,reply=None,thread__subject__contains=request.POST.get('search')).order_by('-date_send')
                    if not message_list:
                        message_list = MessageList.objects.filter(from_user=request.user,saved=True,reply=None,thread__message__contains=request.POST.get('search')).order_by('-date_send')
            #elif request.POST.get
        paginator = Paginator(message_list,15)
        page_num = int(request.GET.get('page',1))
        try:

            page = paginator.page(page_num)
        except (EmptyPage, InvalidPage):
            page = paginator.page(paginator.num_pages)
    gets['search']= search
    get_string="&".join(["%s=%s" % (k, v) for k, v in gets.items()])
    return direct_to_template(request,'mail/draft.html',{'page_obj':page,'search':search,'gets_string':get_string,'msg_list':message_list2,'subject':msg_subject,'flag':flag,'form2':form2,'position':position,'paginator':paginator,'ctr':ctr,'topic_curr_page':page})

@login_required
def notifications(request,message_id=None):
    form2 = SearchNotificationForm()
    position=4
    page = ''
    paginator=''
    ctr = False
    gets={}
    get_string=''
    search = request.GET.get('search')
    if message_id:
        flag = False
        try:
            message_list2 = MessageList.objects.get(thread=message_id,to_user=request.user,reply__isnull=True,notification_type__isnull=False)
        except:
            raise Http404
        page = ''
        
        if message_list2 :
            subject = message_list2.thread.subject
            msg_type = message_list2.message_type
        if msg_type == 1:
           msg_type = 'Pricing'
        elif msg_type==2:
               msg_type = 'Delivery'
        elif msg_type==3:
               msg_type = 'Size&Colours'
        else :
               msg_type = 'Others'
        msg_subject = subject
        msg_subject = msg_type + ' - '+ msg_subject
        if request.POST:
            if request.POST.get('delete'):
                message_list2.saved = False
                message_list2.inbox_deleted=True
                message_list2.send_deleted=True
            return HttpResponseRedirect(reverse('inbox4',args=('',)))
        message_list2.notification_read=True
        message_list2.save()
    else:
        subject = None
        flag = True
        message_list2 = None
        msg_subject = None
        message_list = MessageList.objects.filter(to_user=request.user,reply__isnull=True,inbox_deleted=False,send_deleted=False).exclude(notification_type__isnull=True).order_by('-date_send')
        if request.POST :
            if not request.POST.get('searched'):
                for data in request.POST.getlist('topics'):
                    thread_change = MessageList.objects.get(pk=int(data))
                    if request.POST.get('delete'):
                        thread_change.send_deleted=True
                        thread_change.save()
                    else:
                        return HttpResponseRedirect(reverse('inbox4',args=('',)))
                
                try:
                    message_list = MessageList.objects.filter(to_user=request.user,notification_type=int(request.POST.get('select')),reply__isnull=True,notification_type__isnull=False).order_by('-date_send')
                except:
                    message_list = MessageList.objects.filter(to_user=request.user,reply__isnull=True,send_deleted=False,notification_type__isnull=False)
                #raise Exception(message_list)
            if request.POST.get('searched'):
                    search = request.POST.get('search')

                    message_list = MessageList.objects.filter(to_user=request.user,reply=None,to_user__username__contains=request.POST.get('search'),notification_type__isnull=False).order_by('-date_send')
                    if not message_list :
                        message_list = MessageList.objects.filter(to_user=request.user,reply=None,thread__subject__contains=request.POST.get('search'),notification_type__isnull=False).order_by('-date_send')
                    if not message_list:
                        message_list = MessageList.objects.filter(to_user=request.user,reply=None,thread__message__contains=request.POST.get('search'),notification_type__isnull=False).order_by('-date_send')
        paginator = Paginator(message_list,15)
        page_num = int(request.GET.get('page',1))
        try:

            page = paginator.page(page_num)
        except (EmptyPage, InvalidPage):
            page = paginator.page(paginator.num_pages)
    gets['search']= search
    get_string="&".join(["%s=%s" % (k, v) for k, v in gets.items()])
    return direct_to_template(request,'mail/notification.html',{'page_obj':page,'search':search,'gets_string':get_string,'msg_list':message_list2,'subject':msg_subject,'flag':flag,'form2':form2,'position':position,'paginator':paginator,'ctr':ctr})

def user_lookup(request):
    # Default return list
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            model_results = User.objects.filter(first_name__istartswith=str(value)).order_by('first_name')
            if not model_results:
                model_results = User.objects.filter(last_name__istartswith=str(value)).order_by('first_name')
            if not model_results:
                model_results = Store.objects.filter(name__istartswith=str(value)).order_by('name')
    return direct_to_template(request,'mail/all_user.html',{'users':model_results,})