from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic.simple import direct_to_template
from django.conf import settings
from flash_xml import flash_xml
from forms import FormAddZipFile,FormAddZipFileManual
from models import FlashPageFlip
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import os

def test(request,id,slug=None):
    pages = get_object_or_404(FlashPageFlip,pk=id)
    return direct_to_template (request,'pageflips/Default.html',{'pages':pages,})

def test2(request,id=None,slug=None):
    return HttpResponseRedirect('/media/swf/Pages.swf')

@login_required
def add_file_zip(request,type):
    if request.FILES or request.method == 'POST':
        if FlashPageFlip.STATUS_DICT[type]==1:#zip file
            form = FormAddZipFile(request.POST, request.FILES)
        elif FlashPageFlip.STATUS_DICT[type]==2:#manual
            form = FormAddZipFileManual(request.POST)
        else:
            raise Http404
        
        if form.is_valid():
            if FlashPageFlip.STATUS_DICT[type]==1:#zip file
                file = request.FILES['file']
                filename=(request.FILES['file'].name).split('.')[0]                
            elif FlashPageFlip.STATUS_DICT[type]==2:#manual
                path = form.cleaned_data.get('file_path')
                filename=path.split('.')[0].split('/')[-1]                
                file = os.path.join(settings.BASE_DIR, path)
            
            #xml_path = flash_xml(filename, file)
            #xml_path = xml_path.split('media/')[1]
            #raise Exception(xml_path)
            #object=FlashPageFlip.objects.create(xml=xml_path,slug=slugify(filename))
            content = flash_xml(filename, file)
            #xml_file.open('r')
            #xml_file.read()            
            
            object=FlashPageFlip(slug=slugify(filename))
            filename=filename+'.xml'
            
            object.xml.save(filename,ContentFile(content),save=True)
            #xml_file.close()
            return HttpResponseRedirect(reverse('add_pageflip',args=(type,)))
    else:
        if FlashPageFlip.STATUS_DICT[type]==1:#zip file
            form = FormAddZipFile()
        elif FlashPageFlip.STATUS_DICT[type]==2:#manual
            form = FormAddZipFileManual()
        else:
            raise Http404
    return direct_to_template(request,'pageflips/add-file-zip.html',{'form':form})

#@login_required
#def add_pageflip_manual(request):
#    if request.method == 'POST':
#        form = FormAddZipFileManual(request.POST)
#        if form.is_valid():
#            path = form.cleaned_data.get('file_path')
#            filename=path.split('.')[0].split('pageflip/')[1]
#            #path = path.replace("/","\\")
#            file = os.path.join(settings.BASE_DIR, path)
#            content = flash_xml(filename, file)
#            object=FlashPageFlip(slug=slugify(filename))
#            filename=filename+'.xml'
#
#            object.xml.save(filename,ContentFile(content),save=True)
#            return HttpResponseRedirect(reverse('add_pageflip_manual'))
#    else:
#        form = FormAddZipFileManual()
#    return direct_to_template(request,'pageflips/add-file-zip.html',{'form':form})
