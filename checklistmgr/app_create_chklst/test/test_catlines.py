import inspect
import json
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse, resolve

from app_create_chklst.forms import CategoryModelForm
from app_user.models import User, Company
from app_create_chklst.models import Category, Line


class TestCategoriesAndLines(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = Client()

    def setUp(self):
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        self.my_company = Company(company_name='toto')
        self.my_company.save()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_URL_list_is_ok(self):
        """
            test reverse and resolve for list categories and lines
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_create_chklst:catlineMgmt')
        assert path == '/app_create_chklst/catlinemgmt/'
        assert resolve(path).view_name == 'app_create_chklst:catlineMgmt'

    def test_URL_createcategory_is_ok(self):
        """
            test reverse and resolve for create category
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_create_chklst:chk-catcreate')
        assert path == '/app_create_chklst/catcreate/'
        assert resolve(path).view_name == 'app_create_chklst:chk-catcreate'

    def test_URL_createline_is_ok(self):
        """
            test reverse and resolve for create category
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_create_chklst:chk-linecreate')
        assert path == '/app_create_chklst/linecreate/'
        assert resolve(path).view_name == 'app_create_chklst:chk-linecreate'

    def test_form_Createcategory_isvalid(self):
        """
        verify the register form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = CategoryModelForm(data={
            'cat_key': "toto",
            'cat_wording': 'Libellé',
            'cat_company': self.my_company,
            'cat_enable': True,
        })
        assert(form.is_valid())

    def test_form_Createcategory_isNOTvalid(self):
        """
        verify the create category form is NOT valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = CategoryModelForm(data={
            'cat_key': "",
            'cat_wording': 'Libellé',
            'cat_company': self.my_company,
            'cat_enable': True,
        })
        assert not (form.is_valid())

    def test_create_category_is_ok(self):
        """
            Verify category creation is OK --> RC = 302 + 1 line in the table
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.c.post("/app_create_chklst/catcreate/", data={'cat_key': 'toto',
                                                                      'cat_wording': 'Libelle',
                                                                      'cat_company': self.my_company.id,
                                                                      'cat_enable': True,
                                                                      })
        categories = Category.objects.all()
        assert response.status_code == 302
        assert categories.count() == 1
        assert response.url == "/app_create_chklst/catmgmt/"


    def test_create_line_is_ok(self):
        """
            Verify category creation is OK --> RC = 301 + 1 line in the table
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.c.post("/app_create_chklst/linecreate/", data={'line_key': 'toto',
                                                                       'line_wording': 'Libelle',
                                                                       'line_company': self.my_company.id,
                                                                       'line_enable': True,
                                                                       'line_type': 'C',
                                                                       })
        lines = Line.objects.all()
        assert response.status_code == 302
        assert lines.count() == 1
        assert response.url == "/app_create_chklst/linemgmt/"

    def test_update_category_is_ok(self):
        """
            Verify category update is OK --> RC = 301 + changed category (cat_key)
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        my_category = Category(cat_key='test1',
                               cat_enable=True,
                               cat_wording="test",
                               cat_company=self.my_company)
        my_category.save()
        response = self.c.post("/app_create_chklst/catupdate/" + str(my_category.id),
                               data={'cat_key': 'test2',
                                     'cat_enable': True,
                                     'cat_wording': "test",
                                     'cat_company': self.my_company.id})
        categories = Category.objects.all()
        assert response.status_code == 302
        assert categories[0].cat_key == "test2"
        assert response.url == "/app_create_chklst/catmgmt/"

    def test_update_line_is_ok(self):
        """
            Verify category update is OK --> RC = 301 + changed line (line_key)
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        my_line = Line(line_key='test1',
                       line_enable=True,
                       line_wording="test",
                       line_company=self.my_company,
                       line_type='C', )
        my_line.save()
        response = self.c.post("/app_create_chklst/lineupdate/" + str(my_line.id),
                               data={'line_key': 'test2',
                                     'line_enable': True,
                                     'line_wording': "test",
                                     'line_company': self.my_company.id,
                                     'line_type': 'C', })
        lines = Line.objects.all()
        assert response.status_code == 302
        assert lines[0].line_key == "test2"
        assert response.url == "/app_create_chklst/linemgmt/"

    def test_delete_category_is_ok(self):
        """
            Verify category delete is OK --> RC = 301 + no line in table
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        my_category = Category(cat_key='test1',
                               cat_enable=True,
                               cat_wording="test",
                               cat_company=self.my_company)
        my_category.save()
        response = self.c.post("/app_create_chklst/catdelete/" + str(my_category.id))
        categories = Category.objects.all()
        assert response.status_code == 302
        assert categories.count() == 0
        assert response.url == "/app_create_chklst/catmgmt/"

    def test_delete_line_is_ok(self):
        """
            Verify category delete is OK --> RC = 301 + no line in table
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        my_line = Line(line_key='test1',
                       line_enable=True,
                       line_wording="test",
                       line_company=self.my_company,
                       line_type='C', )
        my_line.save()
        response = self.c.post("/app_create_chklst/linedelete/" + str(my_line.id))
        lines = Line.objects.all()
        assert response.status_code == 302
        assert lines.count() == 0
        assert response.url == "/app_create_chklst/linemgmt/"
