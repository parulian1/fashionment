from django.test.client import Client
from django.test import TestCase

class SimpleTest(TestCase):
    fixtures = ['test']
    def setUp(self):
        pass
        # Every test needs a client.
        
    def test_compose_message(self):
        c = Client()
        c.post('/account/login/',{'username':'casablanko','password':'yoko11'})
        import os
#        dir = os.path.dirname(__file__)
#        file = os.path.join(dir,'haha.jpeg')
#        i=open(file,'rb')
        response = c.post('/mail/inbox/1/',{
            'to_user':20,
            'subject':'testing',
            'message':1,
            'message_type':1,
        })
#        i.close()
#        add_store_form = response.context['add_store_form']
#        raise Exception(add_store_form.errors)
        self.assertEqual(response.status_code,302)

    def test_reply_inbox(self):
        c = Client()
        c.post('/account/login/',{'username':'casablanko','password':'yoko11'})
        import os
#        dir = os.path.dirname(__file__)
#        file = os.path.join(dir,'haha.jpeg')
#        i=open(file,'rb')
        response = c.post('/mail/inbox/1/',{
            'message':'reply_test',
        })
#        i.close()
#        edit_store_form = response.context['form']
#        raise Exception(edit_store_form.errors)
        self.assertEqual(response.status_code,302)