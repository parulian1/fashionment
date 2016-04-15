from django.test.client import Client
from django.test import TestCase

class SimpleTest(TestCase):
    fixtures = ['test']
    def setUp(self):
        pass
        # Every test needs a client.
        
    def test_login_fail(self):
        c = Client()
        succeed = c.login(username="handy",password="h3andy")
        self.assertFalse(succeed)

    def test_login_success(self):
        c = Client()
        succeed = c.login(username="casablanko",password="yoko11")
        self.assertTrue(succeed)
    def test_sign_up(self):
        from extra.librecaptcha import ReCaptcha
        recaptcha = ReCaptcha()
        print recaptcha.image_url

        user_input = raw_input('Enter ReCaptcha: ')

        c = Client(REMOTE_ADDR='127.0.0.1')
        response = c.post('/account/sign-up/',{
            'username':'name',
            'first_name':'first',
            'last_name':'last',
            'sex':1,
            'interest':'bah',
            'email':'yoyo@ma.com',
            'password':'abc123',
            'confirm_password':'abc123',
            'country':1,
            'province':1,
            'phone_area_code':1,
            'telephone':'12122',
            'handphone':'12313',
            'fax_area_code':1,
            'fax':'123123',
            'street_address':'asdasdsd',
            'post_code':1231,
            'date_of_birth':'1/1/1900',
            'personal_website':'',
            'about_me':'asdasd',
            'picture':'asd',
            'checkbox':True,
            'recaptcha_response_field':user_input,
            'recaptcha_challenge_field':recaptcha.challenge_value
        })

        #add_user_form = response.context[0]['add_user_form']
#        raise Exception(response.context[0]['add_user_form'])
        if user_input:
            self.assertEqual(response.status_code,302)
        else:
            add_user_form = response.context[0]['add_user_form']
            self.assertEqual(response.status_code, 200)
            self.assertTrue('recaptcha' in dict(add_user_form.errors),'Expected Recaptcha Error')
        """
        form = response.context['form']
        self.assertEqual(form.is_valid(),True,form.errors)

        sub_user_form = response.context['sub_user_form']
        self.assertEqual(sub_user_form.is_valid(),True,sub_user_form.errors)
        """
    def test_edit_profile(self):
        c = Client()
        c.post('/account/login/',{'username':'casablanko','password':'yoko11'})
        response = c.post('/account/edit-profile/',{
            'first_name':'first',
            'last_name':'last',
            'date_of_birth':'1/1/1900',
            'sex':1,
            'street_address':'bah',
            'country':1,
            'province':1,
            'post_code':1231,
            'phone_area_code':1,
            'telephone':'12122',
            'handphone':'12313',
            'fax_area_code':1,
            'fax':'123123',
            'street_address':'asdasdsd',
            'email':'yoyo@ma.com',
            'personal_website':'',
            'about_me':'asdasd',
            'picture':'asd',
        })
#        edit_my_profile_form = response.context[0]['edit_my_profile_form']
#        raise Exception(edit_my_profile_form.is_valid())
        self.assertEqual(response.status_code,302)
