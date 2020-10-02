import inspect
import json
from django.test import TestCase, Client, TransactionTestCase

from app_user.forms import UserCheckListMgrFormLogin, UserCheckListMgrRegister
from app_user.models import User, UserLanguages



class TestForms(TestCase):
    def setUp(self):
        self.lang = UserLanguages()
        self.lang.code = 'FR'
        self.lang.language = 'Francais'
        self.lang.save()

    def tearDown(self):
        pass

    def test_form_login_isvalid(self):
        """
        verify the login form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = UserCheckListMgrFormLogin(data={
            'username': 'toto',
            'password': 'titi'
        })
        assert(form.is_valid())

    def test_form_register_isvalid(self):
        """
        verify the register form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = UserCheckListMgrRegister(data={
            'preferred_language': self.lang,
            'username': 'toto2',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'toto@toto.fr',
            'password': '12345678',
            'confirm_password': '12345678',
            'phone': '12345',
            'picture': None,
            'user_company': None,
            'admin': False
        })
        assert(form.is_valid())

    def test_form_register_is_notvalid(self):
        """
        verify the register form is not valid if bad input
        """
        print(inspect.currentframe().f_code.co_name)
        form = UserCheckListMgrRegister(data={
            'preferred_language': self.lang,
            'username': 'toto2',
            'first_name': None,
            'last_name': 'lastname',
            'email': 'toto@toto.fr',
            'password': '12345678',
            'confirm_password': '12345678',
            'phone': '12345',
            'picture': None,
            'user_company': None,
            'admin': False
        })
        assert(form.is_valid()) is False

class TestLogin(TestCase):
    def setUp(self):
        self.lang = UserLanguages()
        self.lang.code = 'FR'
        self.lang.language = 'Francais'
        self.lang.save()
        self.user = User.objects.create(preferred_language=self.lang,
                                   username='toto2',
                                   first_name='firstname',
                                   last_name='lastname',
                                   email='toto@toto.fr',
                                   phone='12345',
                                   picture=None,
                                   user_company=None,
                                   admin=False)
        self.user.set_password("12345678")
        self.user.save()
        self.c = Client()

    def tearDown(self):
        pass

    def test_user_login_OK(self):
        """
        Verify login is OK if user/psw is good
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post('/app_home/index/', {'username': 'toto2',
                                                   'password': '12345678',
                                                    'bot_catcher': '', })
        assert response.status_code == 302


    def test_user_login_not_OK(self):
        """
        Verify login is !OK if user/psw is bad
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post('/app_home/index/', {'username': 'toto2',
                                                   'password': '1234567',
                                                    'bot_catcher': '', })
        assert response.status_code == 200


class TestRegister(TransactionTestCase):
    def setUp(self):
        self.lang = UserLanguages()
        self.lang.code = 'FR'
        self.lang.language = 'Francais'
        self.lang.save()
        self.c = Client()

    def tearDown(self):
        pass

    def test_register_OK(self):
        """
        Verify register is OK
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post("/app_user/register/", {'preferred_language': self.lang,
            'username': 'toto32',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'toto@toto.fr',
            'password': '12345678',
            'confirm_password': '12345678',
            'phone': '12345',
            'picture': '',
            'company': '',
            'admin': False
        })
        assert response.status_code == 200
        assert '-RegisterOK-' in response.content.decode('ascii')

    def test_register_not_OK(self):
        """
        Verify register is !OK if psw != psw_confirm
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post("/app_user/register/", {'preferred_language': self.lang,
                                                       'username': 'toto33',
                                                       'first_name': 'firstname',
                                                       'last_name': 'lastname',
                                                       'email': 'toto@toto.fr',
                                                       'password': '12345678',
                                                       'confirm_password': '123456789',
                                                       'phone': '12345',
                                                       'picture': '',
                                                       'company': '',
                                                       'admin': False
                                                       })
        assert response.status_code == 200
        assert '-Errpswconfir-' in response.content.decode('ascii')


class TestDeleteUser(TransactionTestCase):
    def setUp(self):
        self.lang = UserLanguages()
        self.lang.code = 'FR'
        self.lang.language = 'Francais'
        self.lang.save()
        self.user = User.objects.create(preferred_language=self.lang,
                                   username='toto1',
                                   first_name='firstname',
                                   last_name='lastname',
                                   email='toto@toto.fr',
                                   phone='12345',
                                   picture=None,
                                   user_company=None,
                                   admin=False)
        self.user.set_password("12345678")
        self.user.save()
        self.user = User.objects.create(preferred_language=self.lang,
                                        username='toto2',
                                        first_name='firstname',
                                        last_name='lastname',
                                        email='toto2@toto.fr',
                                        phone='12345',
                                        picture=None,
                                        user_company=None,
                                        admin=False)
        self.user.set_password("12345678")
        self.user.save()
        self.c = Client()

    def tearDown(self):
        pass

    def test_delete_user(self):
        """
        Verify if delete user is OK
        First connect then get the user_to_delete's id
        call the ajax function and verify return code and message returned
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.login(username='toto1', password='12345678')
        user_to_delete = User.objects.get(username='toto2')
        id = user_to_delete.id
        data = {'id': id}
        data = json.dumps(data)
        response = self.c.post("/app_user/delete_user/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"OK"' in response.content.decode('ascii')

