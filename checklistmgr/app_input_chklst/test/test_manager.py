import inspect

from django.test import Client, TransactionTestCase
from django.urls import reverse, resolve

from app_input_chklst.models import Manager
from app_user.models import User, Company, Address


class Testmanagers(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = Client()

    def setUp(self):
        self.my_company = Company(company_name='toto')
        self.my_company.save()
        self.my_manager = Manager(mgr_name='mymanager',mgr_company=self.my_company)
        self.my_manager.save()
        self.my_address = Address(address_name='toto',
                                  street_number=5,
                                  address1='Address1',
                                  address2='address2',
                                  zipcode='zip',
                                  city='City',
                                  country='FR', )
        self.my_address.save()

        self.user = User.objects.create_user(username='testuser',
                                             password='toto',
                                             admin=True,
                                             user_company=self.my_company)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_URL_mgmt_manager_is_ok(self):
        """
            test reverse and resolve for mgmt manager
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-mgrmgmt')
        assert path == '/app_input_chklst/managermgmt/'
        assert resolve(path).view_name == 'app_input_chklst:inp-mgrmgmt'

    def test_URL_delete_manager_is_ok(self):
        """
            test reverse and resolve for remove manager
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-mgrdelete', args=[5])
        assert path == '/app_input_chklst/managerdelete/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-mgrdelete'

    def test_URL_display_manager_is_ok(self):
        """
            test reverse and resolve for display manager
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-mgrdisplay', args=[5])
        assert path == '/app_input_chklst/managerdisplay/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-mgrdisplay'

    def test_URL_update_manager_is_ok(self):
        """
            test reverse and resolve for update manager
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-mgrupdate', args=[5])
        assert path == '/app_input_chklst/managerupdate/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-mgrupdate'

    def test_VIEW_create_manager_is_ok(self):
        """
            Verify manager creation is OK --> RC = 302 + 1 more manager in the table
        """
        print(inspect.currentframe().f_code.co_name)
        data = {'mgr_name': 'toto',
                'mgr_contact': 'contact',
                'mgr_phone': '123456',
                'mgr_email1': 'email@toto.fr',
                'mgr_email2': 'email2@toto.fr',
                'mgr_enable': True,
                'mgr_address': self.my_address.id,
                'mgr_company': self.my_company.id}
        self.c.login(username='testuser', password='toto')
        nb1 = Manager.objects.all().count()
        response = self.c.post("/app_input_chklst/managercreate/", data)
        nb2 = Manager.objects.all().count()
        assert response.status_code == 302
        assert nb1 + 1 == nb2

    def test_VIEW_create_manager_is_NOTok(self):
        """
            Verify manager creation is NOT OK --> RC = 200 and same number of lines --> duplicate
        """
        print(inspect.currentframe().f_code.co_name)
        data = {'mgr_name': 'mymanager',
                'mgr_contact': 'contact',
                'mgr_phone': '123456',
                'mgr_email1': 'email@toto.fr',
                'mgr_email2': 'email2@toto.fr',
                'mgr_enable': True,
                'mgr_address': self.my_address.id,
                'mgr_company': self.my_company.id}
        self.c.login(username='testuser', password='toto')
        nb1 = Manager.objects.all().count()
        response = self.c.post("/app_input_chklst/managercreate/", data)
        nb2 = Manager.objects.all().count()
        assert response.status_code == 200
        assert nb1 == nb2

    def test_VIEW_update_manager_is_ok(self):
        """
            Verify manager update is OK --> RC = 302 + updated manager
        """
        print(inspect.currentframe().f_code.co_name)
        data = {'mgr_name': 'mymanager',
                'mgr_contact': 'contact',
                'mgr_phone': '123456',
                'mgr_email1': 'email@toto.fr',
                'mgr_email2': 'email2@toto.fr',
                'mgr_enable': False,
                'mgr_address': self.my_address.id,
                'mgr_company': self.my_company.id}
        self.c.login(username='testuser', password='toto')
        response = self.c.post("/app_input_chklst/managerupdate/" + str(self.my_manager.id), data)
        updated_manager = Manager.objects.get(mgr_name='mymanager')
        assert response.status_code == 302
        assert not updated_manager.mgr_enable
