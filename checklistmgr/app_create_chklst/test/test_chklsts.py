import inspect
import json
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse, resolve

from app_create_chklst.forms import CategoryModelForm, CheckListCreateForm
from app_user.models import User, Company
from app_create_chklst.models import CheckList


class TestCategoriesAndLines(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = Client()

    def setUp(self):
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        self.my_company = Company(company_name='toto')
        self.my_company.save()

        self.my_checklist = CheckList(chk_key="toto2",
                                      chk_title='Libellé',
                                      chk_company=self.my_company,
                                      chk_enable=True,)
        self.my_checklist.save()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_URL_create_chklst_is_ok(self):
        """
            test reverse and resolve for create checklist
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_create_chklst:chk-chklstcreate')
        assert path == '/app_create_chklst/chkcreate/'
        assert resolve(path).view_name == 'app_create_chklst:chk-chklstcreate'

    def test_URL_delete_chklst_is_ok(self):
        """
            test reverse and resolve for remove checklist
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_create_chklst:chk-chkdelete', args=[5])
        assert path == '/app_create_chklst/chklstdelete/5'
        assert resolve(path).view_name == 'app_create_chklst:chk-chkdelete'

    def test_URL_display_chklst_is_ok(self):
        """
            test reverse and resolve for display checklist
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_create_chklst:chk-chkdisplay', args=[5])
        assert path == '/app_create_chklst/chklstdisplay/5'
        assert resolve(path).view_name == 'app_create_chklst:chk-chkdisplay'

    def test_URL_update_chklst_is_ok(self):
        """
            test reverse and resolve for display checklist
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_create_chklst:chk-chkupdate', args=[5])
        assert path == '/app_create_chklst/chklstupdate/5'
        assert resolve(path).view_name == 'app_create_chklst:chk-chkupdate'

    def test_URL_ajax_chklst_is_ok(self):
        """
            test reverse and resolve for display checklist
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_create_chklst:create_chklst')
        assert path == '/app_create_chklst/create_chklst/'
        assert resolve(path).view_name == 'app_create_chklst:create_chklst'

    def test_form_Createchklst_isvalid(self):
        """
        verify the create checklist form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = CheckListCreateForm(data={
            'chk_key': "toto",
            'chk_title': 'Libellé',
            'chk_company': self.my_company,
            'chk_enable': True,
        })
        assert(form.is_valid())

    def test_form_Createchklst_isNOTvalid(self):
        """
        verify the create checklist form is NOT valid --> invalid data
        """
        print(inspect.currentframe().f_code.co_name)
        form = CheckListCreateForm(data={
            'chk_key': "toto",
            'chk_title': 'Libellé',
            'chk_company': 45,
            'chk_enable': True,
        })
        assert not (form.is_valid())

    def test_create_checklist_is_ok(self):
        """
            Verify checklist creation is OK --> RC = 200 + 1 more line in the table
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        nb1 = CheckList.objects.all().count()
        data = {'chk_key': 'toto', 'chk_title': 'Libelle', 'chk_company': self.my_company.id, 'chk_enable': True,
                'lines': [], 'action': 'create'}
        data = json.dumps(data)
        response = self.c.post("/app_create_chklst/create_chklst/", data, content_type="application/json")
        nb2 = CheckList.objects.all().count()
        assert response.status_code == 200
        assert '"OK"' in response.content.decode('ascii')
        assert nb1 + 1 == nb2

    def test_create_checklist_is_NOTok(self):
        """
            Verify checklist creation is NOT OK --> RC = 200 but same number of lines
        """
        print(inspect.currentframe().f_code.co_name)
        nb1 = CheckList.objects.all().count()
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        data = {'chk_key': 'toto2', 'chk_title': 'Libelle', 'chk_company': self.my_company.id, 'chk_enable': True,
                'lines': [], 'action': 'create'}
        data = json.dumps(data)
        response = self.c.post("/app_create_chklst/create_chklst/", data, content_type="application/json")
        nb2 = CheckList.objects.all().count()
        assert response.status_code == 200
        assert nb1 == nb2

    def test_update_checklist_is_ok(self):
        """
            Verify checklist update is OK --> RC = 200 + updated line
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        data = {'chk_key': 'toto2', 'chk_title': 'NEW', 'chk_company': self.my_company.id, 'chk_enable': True,
                'lines': [], 'action': 'update'}
        data = json.dumps(data)
        response = self.c.post("/app_create_chklst/create_chklst/", data, content_type="application/json")
        updated_checklist = CheckList.objects.get(chk_key='toto2')
        assert response.status_code == 200
        assert '"OK"' in response.content.decode('ascii')
        assert updated_checklist.chk_title == 'NEW'
