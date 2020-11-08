import inspect
import json
from django.test import TestCase, Client, TransactionTestCase, RequestFactory
from django.urls import reverse, resolve

from app_create_chklst.forms import CategoryModelForm
from app_create_chklst.views import CategoryCreateView, LineCreateView, CategoryUpdateView, LineUpdateView, \
    CategoryDeleteView, LineDeleteView, CategoryDisplayView, LineDisplayView, CatandLineMgmtView, CategoryMgmtView, \
    LineMgmtView
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

    def test_FORM_Createcategory_isvalid(self):
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

    def test_FORM_Createcategory_isNOTvalid(self):
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

    def test_VIEW_create_category_is_ok(self):
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

    def test_VIEW_create_category_is_NOTok(self):
        """
            Verify category creation is NOT OK --> RC = 200 + error msg
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        Category.objects.create(cat_key='toto', cat_company=self.my_company)
        response = self.c.post("/app_create_chklst/catcreate/", data={'cat_key': 'toto',
                                                                      'cat_wording': 'Libelle',
                                                                      'cat_company': self.my_company.id,
                                                                      'cat_enable': True,
                                                                      })

        assert response.status_code == 200
        assert "Category with this Category key" in response.content.decode('ascii')



    def test_VIEW_create_line_is_ok(self):
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

    def test_VIEW_create_line_is_NOTok(self):
        """
            Verify category creation is NOT OK --> RC = 200 + error display
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        Line.objects.create(line_key='toto', line_company=self.my_company)
        response = self.c.post("/app_create_chklst/linecreate/", data={'line_key': 'toto',
                                                                       'line_wording': 'Libelle',
                                                                       'line_company': self.my_company.id,
                                                                       'line_enable': True,
                                                                       'line_type': 'C',
                                                                       })
        assert response.status_code == 200
        assert "Line with this Line key" in response.content.decode('ascii')


    def test_VIEW_update_category_is_ok(self):
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

    def test_VIEW_update_line_is_ok(self):
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

    def test_VIEW_delete_category_is_ok(self):
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

    def test_VIEW_delete_line_is_ok(self):
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

class test_VIEW_GET_Method(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(test_VIEW_GET_Method, cls).setUpClass()
        cls.c = Client()

    def setUp(self):
        self.my_company = Company.objects.create(company_name='toto')
        self.user = User.objects.create_user(username='testuser2',
                                             password='toto',
                                             admin=True,
                                             user_company=self.my_company,
                                             email="toto@tutu.fr")
        self.my_category = Category.objects.create(cat_key='test1',
                                                   cat_enable=True,
                                                   cat_wording="test",
                                                   cat_company=self.my_company)
        self.my_line = Line.objects.create(line_key='test1',
                                           line_enable=True,
                                           line_wording="test",
                                           line_company=self.my_company,
                                           line_type='C', )
        self.my_company.save()
        self.my_category.save()
        self.user.save()
        self.my_line.save()

    def test_VIEW_CategoryCreateView_isOK(self):
        """
        verify view CategoryCreateView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = CategoryCreateView()
        view.setup(request)
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/createcategory.html']

    def test_VIEW_LineCreateView_isOK(self):
        """
        verify view LineCreateView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = LineCreateView()
        view.setup(request)
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/createline.html']

    def test_VIEW_CategoryUpdateView_isOK(self):
        """
        verify view CategoryUpdateView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = CategoryUpdateView()
        view.setup(request, pk=self.my_category.id)
        request.session = self.c.session
        request.user = self.user
        # request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/updatecategory.html']

    def test_VIEW_LineUpdateView_isOK(self):
        """
        verify view LineUpdateView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = LineUpdateView()
        view.setup(request, pk=self.my_line.id)
        request.session = self.c.session
        request.user = self.user
        # request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/updateline.html']

    def test_VIEW_CategoryDeleteView_isOK(self):
        """
        verify view CategoryDeleteView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = CategoryDeleteView()
        view.setup(request, pk=self.my_category.id)
        request.session = self.c.session
        request.user = self.user
        # request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/deletecategory.html']

    def test_VIEW_LineDeleteView_isOK(self):
        """
        verify view LineDeleteView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = LineDeleteView()
        view.setup(request, pk=self.my_category.id)
        request.session = self.c.session
        request.user = self.user
        # request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/deleteline.html']

    def test_VIEW_LineUpdateView_isOK(self):
        """
        verify view LineUpdateView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = LineUpdateView()
        view.setup(request, pk=self.my_line.id)
        request.session = self.c.session
        request.user = self.user
        # request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/updateline.html']

    def test_VIEW_CategoryDisplayView_isOK(self):
        """
        verify view CategoryDisplayView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = CategoryDisplayView()
        view.setup(request, pk=self.my_category.id)
        request.session = self.c.session
        request.user = self.user
        # request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/displaycategory.html']

    def test_VIEW_LineDisplayView_isOK(self):
        """
        verify view LineDisplayView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = LineDisplayView()
        view.setup(request, pk=self.my_line.id)
        request.session = self.c.session
        request.user = self.user
        # request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert context.template_name == ['app_create_chklst/dialogboxes/displayline.html']

    def test_VIEW_CategoryMgmtView_isOK(self):
        """
        verify view CategoryMgmtView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = CategoryMgmtView()
        view.setup(request)
        request.session = self.c.session
        request.user = self.user
        context = view.get(request)
        assert context.status_code == 200
        assert 'app_create_chklst/categorymgmt.html' in context.template_name
        result = view.get_queryset()
        assert result.count() == 1
        context = view.get_context_data()
        assert context['title'] == 'Categories'

    def test_VIEW_LineMgmtView_isOK(self):
        """
        verify view LineMgmtView - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = LineMgmtView()
        view.setup(request)
        request.session = self.c.session
        request.user = self.user
        context = view.get(request)
        assert context.status_code == 200
        assert 'app_create_chklst/linemgmt.html' in context.template_name
        result = view.get_queryset()
        assert result.count() == 1
        context = view.get_context_data()
        assert context['title'] == 'Lines'

    def test_VIEW_CatandLineMgmtView_is_ok(self):
        """
            Verify CatandLineMgmtView is OK --> get & post
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.c.get("/app_create_chklst/catlinemgmt/")
        assert response.status_code == 200
        response = self.c.post("/app_create_chklst/catlinemgmt/")
        assert response.status_code == 200
