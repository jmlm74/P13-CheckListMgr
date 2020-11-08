import inspect
import json

from django.urls import reverse, resolve
from django.test import RequestFactory, TestCase, Client, TransactionTestCase

from app_checklist.models import CheckListDone
from app_create_chklst.models import CheckList
from app_home.views import LegalView, ContactView, Index
from app_input_chklst.models import Manager, Material
from app_user.models import User, Company


class TestUrls(TestCase):
    """
        Test urls for home_app
    """

    def test_URL_index_is_ok(self):
        """
            test reverse and resolve for /
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('index')
        assert path == '/'
        assert resolve(path).view_name == 'index'

    def test_URL_apphome_index_is_ok(self):
        """
            test reverse and resolve for app_home/index/
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_home:index')
        assert path == '/app_home/index/'
        assert resolve(path).view_name == 'app_home:index'

    def test_URL_legal_ok(self):
        """
            test reverse and resolve for Legal
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_home:legal')
        assert path == '/app_home/legal/'
        assert resolve(path).view_name == 'app_home:legal'

    def test_URL_contact_ok(self):
        """
            test reverse and resolve for contact
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_home:contact')
        assert path == '/app_home/contact/'
        assert resolve(path).view_name == 'app_home:contact'

class LegalViewBasedViewTest(TestCase):
    """
    Test legalView
    """
    def test_VIEW_LegalView_is_OK(self):
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = LegalView()
        view.setup(request)
        assert view.template_name == 'app_home/legal.html'


class ContactViewBasedViewTest(TestCase):
    """
    Test ContactView
    """
    def test_VIEW_ContactView_is_OK(self):
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = ContactView()
        view.setup(request)
        assert view.template_name == 'app_home/contact.html'


class IndexViewBasedViewTest(TestCase):
    """
    Test ContactView
    """
    def test_VIEW_IndexView_is_OK(self):
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = Index()
        view.setup(request)
        assert view.template_name == 'app_home/home.html'


class SearchTest(TransactionTestCase):
    def setUp(self):
        self.my_company = Company.objects.create(company_name='toto')
        self.my_company2 = Company.objects.create(company_name='toto2')
        self.my_manager = Manager.objects.create(mgr_name='mymanager', mgr_company=self.my_company)
        self.my_manager2 = Manager.objects.create(mgr_name='mymanager2', mgr_company=self.my_company)
        self.my_checklist = CheckList.objects.create(chk_key="toto2",
                                                     chk_title='Libellé',
                                                     chk_company=self.my_company,
                                                     chk_enable=True, )
        self.my_material = Material.objects.create(mat_designation="mymaterial",
                                                   mat_registration='Libellé',
                                                   mat_type="zzz",
                                                   mat_model="aaa",
                                                   mat_enable=True,
                                                   mat_company=self.my_company,
                                                   mat_manager=self.my_manager, )
        self.my_material2 = Material.objects.create(mat_designation="mamaterial2",
                                                    mat_registration='Libellé',
                                                    mat_type="zzz",
                                                    mat_model="aaa",
                                                    mat_enable=True,
                                                    mat_company=self.my_company,
                                                    mat_manager=self.my_manager, )

        self.c = Client()

    def test_VIEW_autocomplete_search_mat_is_OK(self):
        """"
        verify  Ajax autocomplete_search_mat is OK
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser', user_company=self.my_company)[0])
        data = {'manager': self.my_manager.id, }
        data = json.dumps(data)
        response = self.c.post("/app_home/autocomplete_search_mat/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"mymaterial"' in response.content.decode("utf-8")

    def test_VIEW_autocomplete_search_man_is_OK(self):
        """"
        verify  Ajax autocomplete_search_man is OK
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser', user_company=self.my_company)[0])
        data = {'material': self.my_material.id, }
        data = json.dumps(data)
        response = self.c.post("/app_home/autocomplete_search_man/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"mymanager"' in response.content.decode("utf-8")

class SearchChklstTest(TransactionTestCase):
    def setUp(self):
        self.my_company = Company.objects.create(company_name='toto')
        self.my_company2 = Company.objects.create(company_name='toto2')
        self.my_manager = Manager.objects.create(mgr_name='mymanager', mgr_company=self.my_company)
        self.my_manager2 = Manager.objects.create(mgr_name='mymanager2', mgr_company=self.my_company)
        self.my_checklist = CheckList.objects.create(chk_key="toto2",
                                                     chk_title='Libellé',
                                                     chk_company=self.my_company,
                                                     chk_enable=True, )
        self.my_material = Material.objects.create(mat_designation="mymaterial",
                                                   mat_registration='Libellé',
                                                   mat_type="zzz",
                                                   mat_model="aaa",
                                                   mat_enable=True,
                                                   mat_company=self.my_company,
                                                   mat_manager=self.my_manager, )
        self.my_material2 = Material.objects.create(mat_designation="mamaterial2",
                                                    mat_registration='Libellé',
                                                    mat_type="zzz",
                                                    mat_model="aaa",
                                                    mat_enable=True,
                                                    mat_company=self.my_company,
                                                    mat_manager=self.my_manager, )
        self.c = Client()
        self.user = self.c.force_login(User.objects.get_or_create(username='testuser', user_company=self.my_company)[0])
        self.new_chklst_done = CheckListDone.objects.create(cld_status=1,
                                                            cld_key='unique_key',
                                                            cld_pdf_file="fic.pdf",
                                                            cld_valid=True,
                                                            cld_user=self.user,
                                                            cld_checklist=self.my_checklist,
                                                            cld_material=self.my_material,
                                                            cld_manager=self.my_manager,
                                                            cld_company=self.my_company)
        self.new_chklst_done2 = CheckListDone.objects.create(cld_status=1,
                                                             cld_key='unique_key2',
                                                             cld_pdf_file="fic.pdf",
                                                             cld_valid=True,
                                                             cld_user=self.user,
                                                             cld_checklist=self.my_checklist,
                                                             cld_material=self.my_material2,
                                                             cld_manager=self.my_manager,
                                                             cld_company=self.my_company)


    def test_VIEW_autocomplete_search_chklst_1param_is_OK(self):
        """"
        verify  Ajax search_chklst material parameter is OK --> returns 1 chklst
        """
        print(inspect.currentframe().f_code.co_name)
        data = {'material': self.my_material.id, }
        data = json.dumps(data)
        response = self.c.post("/app_home/search_chklst/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"unique_key"' in response.content.decode("utf-8")
        assert '"unique_key2"' not in response.content.decode("utf-8")

    def test_VIEW_autocomplete_search_chklst_2returns_is_OK(self):
        """"
        verify  Ajax search_chklst parameter manager is OK (parameter manager --> returns 2 checklists)
        """
        print(inspect.currentframe().f_code.co_name)
        data = {'manager': self.my_manager.id, }
        data = json.dumps(data)
        response = self.c.post("/app_home/search_chklst/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"unique_key"' in response.content.decode("utf-8")
        assert '"unique_key2"' in response.content.decode("utf-8")
