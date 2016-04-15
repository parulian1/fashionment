import os.path, os , zipfile
from django.conf import settings
from django.core.files import File
def unzip_file_into_dir(file, dir):
    zfobj = zipfile.ZipFile(file)
    for name in zfobj.namelist():
        if name.endswith('/'):
            os.mkdir(os.path.join(dir, name))
        else:
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

def flash_xml(filename,file_zip):
#    #get all files in pages_dir
#    all_page_image=os.listdir(pages_dir)
#
#    #clear all files that in pages_dir
#    for file in all_page_image:
#        os.remove(os.path.join(pages_dir, file))
    #unzip the zip file and put it on pages folder
    pageflip_folder = os.path.join(settings.MEDIA_ROOT,'pageflip')
    if not os.path.exists(pageflip_folder):
        os.mkdir(pageflip_folder, 0777)

    filename_dir = os.path.join(pageflip_folder,filename)
    if not os.path.exists(filename_dir):
        os.mkdir(filename_dir, 0777)

    unzip_file_into_dir(file_zip, filename_dir)
    all_page_image=sorted(os.listdir(filename_dir))
    xml_file=os.path.join(pageflip_folder,filename+'.xml')

    #create_file_xml = open(xml_file,"w")
    #file = File(create_file_xml)
    #file.open(mode=None)
    
    content_xml = '<content width="724" height="1024" bgcolor="cccccc" loadercolor="ffffff" panelcolor="5d5d61" buttoncolor="5d5d61" textcolor="ffffff">'

    for page in all_page_image:
        if not page == 'Thumbs.db':
            #page = string(page)
            content_xml+='<page src="'+settings.MEDIA_URL+'pageflip/'+filename+'/'+page+'"/>'
    content_xml+='</content>'
    content_xml=str(content_xml)
    #file.write(content_xml)
    #file.close()
    return content_xml
