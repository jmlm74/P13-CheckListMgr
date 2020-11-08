from django.test import TestCase, Client, TransactionTestCase, RequestFactory
from django.urls import reverse, resolve
import inspect

from app_user.company_views import ListCompaniesView, CreateCompanyView, EditCompanyView
from app_user.models import User, Company, Address


class TestCompany(TransactionTestCase):
    """
        Test urls for app_user- company
    """
    @classmethod
    def setUp(self):
        self.c = Client()
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        self.my_company = Company.objects.create(company_name='toto')


    def test_URL_create_company_is_ok(self):
        """
            test reverse and resolve for create company
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_user:createcompany')
        assert path == '/app_user/create_company/'
        assert resolve(path).view_name == 'app_user:createcompany'

    def test_URL_update_company_is_ok(self):
        """
            test reverse and resolve for update company
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_user:editcompany', kwargs={'pk':1})
        assert path == '/app_user/update/1'
        assert resolve(path).view_name == 'app_user:editcompany'

    def test_VIEW_CreateCompanyView_isOK(self):
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = CreateCompanyView()
        view.setup(request)
        request.session = self.c.session
        request.user = self.c.force_login(User.objects.get_or_create(username='testuser')[0])

        context = view.get(request)
        assert context.status_code == 200
        assert view.template_name == 'app_user/create_company.html'

    def test_VIEW_createcompany_is_OK(self):
        """
        Verify company creation is OK --> RC = 200 + RegisterOK in response.content
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        nb1 = Company.objects.all().count()
        response = self.c.post("/app_user/create_company/", {'company_name': 'toti',
                                                             'address_name': 'address',
                                                             'street_number': 5,
                                                             'street_type': 'rue',
                                                             'address1': 'ligne1',
                                                             'address2': 'ligne2',
                                                             'zipcode': 'zip',
                                                             'city': 'Paris',
                                                             'country': 'France',
                                                             })
        nb2 = Company.objects.all().count()
        assert response.status_code == 200
        assert nb2 == nb1 + 1
        assert '-RegisterOK-' in response.content.decode('ascii')


    def test_VIEW_createcompany_is_NOT_OK(self):
        """
        Verify company creation is OK --> RC = 200 + RegisterOK in response.content
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post("/app_user/create_company/", {'company_name': 'toto',
                                                             'address_name': 'address',
                                                             'street_number': 5,
                                                             'street_type': 'rue',
                                                             'address1': 'ligne1',
                                                             'address2': 'ligne2',
                                                             'zipcode': 'zip',
                                                             'city': 'Paris',
                                                             'country': 'France',
                                                             })
        assert response.status_code == 200
        assert 'Company with this Society already exists.' in response.content.decode('ascii')


    def test_VIEW_ListCompaniesView_isOK(self):
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = ListCompaniesView()
        view.setup(request)
        assert view.template_name == 'app_user/list_company.html'


class testEditCompany(TransactionTestCase):
    def setUp(self):
        self.new_address = Address.objects.create(address_name='toto',
                                                  street_number=5,
                                                  address1='Address1',
                                                  address2='address2',
                                                  zipcode='zip',
                                                  city='City',
                                                  country='FR', )
        self.my_company = Company.objects.create(company_name='toto', address=self.new_address)
        self.c = Client()
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_VIEW_EditCompanyView_isOK(self):
        print(inspect.currentframe().f_code.co_name)

        request = RequestFactory().get('/')
        view = EditCompanyView()
        view.setup(request, pk=self.my_company.id)
        request.session = self.c.session
        request.user = self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        context = view.get(request)
        assert context.status_code == 200
        assert view.template_name == 'app_user/create_company.html'

    def test_VIEW_EditCompany_isOK(self):
        """
                Verify company creation is OK --> RC = 200 + RegisterOK in response.content
                """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post("/app_user/update/"+str(self.my_company.id), {'company_name': 'toto',
                                                             'address_name': 'address',
                                                             'street_number': 5,
                                                             'street_type': 'rue',
                                                             'address1': 'ligne1',
                                                             'address2': 'ligne2',
                                                             'zipcode': 'zip',
                                                             'city': 'Paris',
                                                             'country': 'France',
                                                             })
        assert response.status_code == 200
        assert "-CompanyupdateOK-" in response.content.decode("utf-8")






