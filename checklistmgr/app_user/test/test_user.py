import inspect
import json
from django.test import TestCase, Client, TransactionTestCase, RequestFactory

from app_user.forms import UserCheckListMgrFormLogin, UserCheckListMgrRegister
from app_user.models import User, UserLanguages, Company
from app_user.views import RegisterView, EditUserView, UserListView, LineDeleteView


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

    def test_FORM_register_isvalid(self):
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

    def test_FORM_register_is_notvalid(self):
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

    def test_VIEW_user_login_OK(self):
        """
        Verify login is OK if user/psw is good
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post('/app_home/index/', {'username': 'toto2',
                                                    'password': '12345678',
                                                    'bot_catcher': '', })
        assert response.status_code == 302


    def test_VIEW_user_login_not_OK(self):
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
        self.my_company = Company.objects.create(company_name='toto')
        self.c = Client()

    def tearDown(self):
        pass

    def test_VIEW_register_part_isOK(self):
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
        request = RequestFactory().get('/')
        view = RegisterView()
        view.setup(request)
        assert view.template_name == 'app_user/register.html'

    def test_VIEW_register_pro_isOK(self):
        """
        Verify register is OK with a pro ser
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
                                                       'company': self.my_company.id,
                                                       'admin': False
                                                       })
        assert response.status_code == 200
        assert '-RegisterOK-' in response.content.decode('ascii')


    def test_VIEW_register_not_OK(self):
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

    def test_VIEW_delete_user_is_OK(self):
        """
        Verify if delete user is OK
        First connect then get the user_to_delete's id
        call the ajax function and verify return code and message returned
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.login(username='toto1', password='12345678')
        user_to_delete = User.objects.get(username='toto2')
        user_id = user_to_delete.id
        data = {'id': user_id}
        data = json.dumps(data)
        response = self.c.post("/app_user/delete_user/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"OK"' in response.content.decode('ascii')


class TestDeleteUser(TransactionTestCase):

    def setUp(self):
        self.my_company = Company.objects.create(company_name='toto')
        self.user = User.objects.create_user(username='testuser2',
                                             password='toto',
                                             admin=True,
                                             user_company=self.my_company,
                                             email="toto@tutu.fr")
        self.c = Client()
        self.c.force_login(User.objects.get_or_create(username='testuser', user_company=self.my_company)[0])

    def test_VIEW_logout_isOK(self):
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post("/app_user/logout/")
        assert response.status_code == 302

    def test_VIEW_edituser_isOK(self):
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = EditUserView()
        view.setup(request)
        assert view.template_name == 'app_user/register.html'

    def test_VIEW_userlist_isOK(self):
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = UserListView()
        view.setup(request)
        request.user = self.user
        response = view.get_queryset()
        assert view.template_name == 'app_user/list.html'
        assert response.count() == 2  # 2 users created !

    def test_VIEW_LineDelete_isOK(self):
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = LineDeleteView()
        view.setup(request)
        assert view.template_name == 'app_user/dialogboxes/deleteuser.html'