from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse, resolve
import inspect
from app_user.models import User


class TestCompany(TransactionTestCase):
    """
        Test urls for app_user- company
    """
    @classmethod
    def setUpClass(cls):
        cls.c = Client()

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

    def test_createcompany_is_OK(self):
        """
        Verify company creation is OK --> RC = 200 + RegisterOK in response.content
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
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
        assert '-RegisterOK-' in response.content.decode('ascii')
