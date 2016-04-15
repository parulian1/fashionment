from django.test.client import Client
from django.test import TestCase

class SimpleTest(TestCase):
    fixtures = ['test']
    def setUp(self):
        pass
        # Every test needs a client.
        
    def test_add_store(self):
        c = Client()
        c.post('/account/login/',{'username':'casablanko','password':'yoko11'})
        import os
        dir = os.path.dirname(__file__)
        file = os.path.join(dir,'haha.jpeg')
        i=open(file,'rb')
        response = c.post('/fashion/store/add-store/',{
            'name':'name',
            'location':'location',
            'country':1,
            'province':1,
            'post_code':12311,
            'phone_area':1,
            'telephone':'12122',
            'handphone':'12313',
            'fax_code':1,
            'fax':'123123',
            'company_website':'',
            'store_story':'asdasd',
            'picture':i,
            'promotion_text':'promotion_text',
        })
        i.close()
#        add_store_form = response.context['add_store_form']
#        raise Exception(add_store_form.errors)
        self.assertEqual(response.status_code,302)

    def test_edit_store(self):
        c = Client()
        c.post('/account/login/',{'username':'casablanko','password':'yoko11'})
        import os
        dir = os.path.dirname(__file__)
        file = os.path.join(dir,'haha.jpeg')
        i=open(file,'rb')
        response = c.post('/fashion/store/edit-store/',{
            'name':'name',
            'location':'location',
            'country':1,
            'province':1,
            'post_code':12311,
            'phone_area':1,
            'telephone':12122,
            'handphone':12313,
            'fax_code':1,
            'fax':123123,
            'company_website':'www.yahoo.com',
            'store_story':'asdasd',
            'picture':i,
            'promotion_text':'promotion_text',
        })
        i.close()
#        edit_store_form = response.context['form']
#        raise Exception(edit_store_form.errors)
        self.assertEqual(response.status_code,302)

    def test_add_line(self):
        c = Client()
        c.post('/account/login/',{'username':'casablanko','password':'yoko11'})
        response = c.post('/fashion/store/add-line/',{
            'line':'line',
            'category':1,
        })
#        add_line_form = response.context['add_line']
#        raise Exception(add_line_form.is_valid())
        self.assertEqual(response.status_code,302)
    def test_add_item(self):
        c = Client()
        c.post('/account/login/',{'username':'casablanko','password':'yoko11'})
        import os
        dir = os.path.dirname(__file__)
        file = os.path.join(dir,'haha.jpeg')
        i=open(file,'rb')
        a=open(file,'rb')
        response = c.post('/fashion/store/add-item/2/',{
            'item_code':'00-11',
            'item':'item',
            'description':"0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789asd",
            'gender':1,
            'color':'red',
            'size':'42 xl',
            'currency':1,
            'price':12321,
            'availability':1,
            'picture1':i,
            'picture2':a,
        })
        i.close()
        a.close()
        #add_store_form = response.context[0]['form']
        #raise Exception(add_store_form.errors)
        self.assertEqual(response.status_code,302)
    def test_edit_item(self):
        c = Client()
        c.post('/account/login/',{'username':'casablanko','password':'yoko11'})
        import os
        dir = os.path.dirname(__file__)
        file = os.path.join(dir,'haha.jpeg')
        i=open(file,'rb')
        a=open(file,'rb')
        response = c.post('/fashion/store/edit-item/2/',{
            'item_code':'00-11',
            'item':'item',
            'description':"asdasd",
            'gender':1,
            'color':'red',
            'size':'42 xl',
            'currency':1,
            'price':12321,
            'availability':1,
            'picture1':i,
            'picture2':a,
        })
        i.close()
        a.close()
#        add_store_form = response.context[0]['edititemform']
#        raise Exception(add_store_form.errors)
        self.assertEqual(response.status_code,302)