import inspect

from django.test import Client, TransactionTestCase
from django.urls import reverse, resolve

from app_input_chklst.forms import AddressCreateForm
from app_user.models import User, Address


class Testaddresses(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = Client()

    def setUp(self):
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_URL_mgmt_address_is_ok(self):
        """
            test reverse and resolve for mgmt address
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-addrmgmt')
        assert path == '/app_input_chklst/addressmgmt/'
        assert resolve(path).view_name == 'app_input_chklst:inp-addrmgmt'

    def test_URL_delete_address_is_ok(self):
        """
            test reverse and resolve for remove address
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-addrdelete', args=[5])
        assert path == '/app_input_chklst/addressdelete/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-addrdelete'

    def test_URL_display_address_is_ok(self):
        """
            test reverse and resolve for display address
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-addrdisplay', args=[5])
        assert path == '/app_input_chklst/addressdisplay/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-addrdisplay'

    def test_URL_update_address_is_ok(self):
        """
            test reverse and resolve for update address
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-addrupdate', args=[5])
        assert path == '/app_input_chklst/addressupdate/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-addrupdate'

    def test_FORM_Createaddress_isvalid(self):
        """
        verify the create address form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = AddressCreateForm(data={'address_name': 'toto',
                                       'street_number': 5,
                                       'address1': 'Address1',
                                       'address2': 'address2',
                                       'zipcode': 'zip',
                                       'city': 'City',
                                       'country': 'FR'
                                       })
        assert(form.is_valid())

    def test_FORM_Createaddress_isNOTvalid(self):
        """
        verify the create address form is NOT valid --> invalid data
        """
        print(inspect.currentframe().f_code.co_name)
        form = AddressCreateForm(data={'address_name': '',
                                       'street_number': '5',
                                       'address1': 'Address1',
                                       'address2': 'address2',
                                       'zipcode': 'zip',
                                       'city': 'City',
                                       'country': 'FR'
                                       })
        assert not (form.is_valid())

    def test_VIEW_create_address_is_ok(self):
        """
            Verify address creation is OK --> RC = 302 + 1 more line in the table
        """
        print(inspect.currentframe().f_code.co_name)
        nb1 = Address.objects.all().count()
        data = {'address_name': 'toto',
                'street_number': 5,
                'address1': 'Address1',
                'address2': 'address2',
                'zipcode': 'zip',
                'city': 'City',
                'country': 'FR'
                }
        response = self.c.post("/app_input_chklst/addresscreate/", data)
        nb2 = Address.objects.all().count()
        assert response.status_code == 302
        assert nb1 + 1 == nb2

    def test_VIEW_create_address_is_NOTok(self):
        """
            Verify address creation is NOT OK --> RC = 200 and same number of lines
        """
        print(inspect.currentframe().f_code.co_name)
        new_address = Address(address_name='toto',
                              street_number=5,
                              address1='Address1',
                              address2='address2',
                              zipcode='zip',
                              city='City',
                              country='FR', )
        new_address.save()

        nb1 = Address.objects.all().count()
        data = {'address_name': '',
                'street_number': '5',
                'address1': 'Address1',
                'address2': 'address2',
                'zipcode': 'zip',
                'city': 'City',
                'country': 'FR'
                }
        response = self.c.post("/app_input_chklst/addresscreate/", data)
        nb2 = Address.objects.all().count()
        assert response.status_code == 200
        assert nb1 == nb2

    def test_VIEW_update_address_is_ok(self):
        """
            Verify address update is OK --> RC = 302 + updated address
        """
        print(inspect.currentframe().f_code.co_name)
        new_address = Address(address_name='toto',
                              street_number=5,
                              address1='Address1',
                              address2='address2',
                              zipcode='zip',
                              city='City',
                              country='FR', )
        new_address.save()
        data = {'address_name': 'titi',
                'street_number': 15,
                'address1': 'Address1',
                'address2': 'address2',
                'zipcode': 'zip',
                'city': 'City',
                'country': 'FR'
                }
        response = self.c.post("/app_input_chklst/addressupdate/" + str(new_address.id), data)

        updated_address = Address.objects.get(address_name='titi')
        assert response.status_code == 302
        assert updated_address.street_number == 15
