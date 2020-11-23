import inspect
import json

from django.template import Context
from django.test import TransactionTestCase, Client, RequestFactory
from app_user.models import Address

from app_user.models import User, UserLanguages, Company
from app_utilities.models import Translation
from app_utilities.templatetags.dis_play import dis_play, dis_play_result, dis_play_remark


class TestUtilities(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = Client()

    def setUp(self):
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        Translation.objects.create(Position='Test', FR='TestFR', UK='TestUK')
        self.my_company = Company.objects.create(company_name='toto')
        self.french = UserLanguages.objects.create(code='FR', language="francais")
        self.uk = UserLanguages.objects.create(code='UK', language="English")
        self.user = User.objects.create_user(username='testuser2',
                                             password='toto',
                                             admin=True,
                                             user_company=self.my_company,
                                             preferred_language=self.french,
                                             email="toto@tutu.fr")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_VIEW_get_message_ok(self):
        print(inspect.currentframe().f_code.co_name)
        response = dis_play(None, "Test")
        assert response == 'TestFR'

    def test_VIEW_dis_play_result_ok(self):
        print(inspect.currentframe().f_code.co_name)
        context = {'dict_choices': {'1-on': '1', '2-off': '2', }}
        result = dis_play_result(context, "1")
        assert result == "valid"

    def test_VIEW_dis_play_remark_ok(self):
        print(inspect.currentframe().f_code.co_name)
        context = {'dict_remarks': {'text-1': 'RemarksOK', 'text-2': 'Remark2-OK', }}
        result = dis_play_remark(context, "2")
        assert result == "Remark2-OK"

    def test_VIEW_get_message_Ajax_is_ok(self):
        """
            Verify if get message returns a good translated message
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        data = {'msg': 'Test',}
        data = json.dumps(data)
        response = self.c.post("/app_utilities/get_message/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"OK"' in response.content.decode('ascii')
        assert '"TestUK"' in response.content.decode('ascii')

    def test_VIEW_get_address_Ajax_is_ok(self):
        """
            Verify if get address returns a good  address
        """
        print(inspect.currentframe().f_code.co_name)
        new_addr = Address.objects.create(address_name='nomaddr',
                                          street_number=1,
                                          street_type="rue",
                                          address1="rue adr1",
                                          address2="",
                                          zipcode="75008",
                                          city="Paris",
                                          country="France")
        new_addr.save()
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        data = {'id': new_addr.id, }
        data = json.dumps(data)
        response = self.c.post("/app_utilities/get_address/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"OK"' in response.content.decode('ascii')
        assert '"address"' in response.content.decode('ascii')

    def test_VIEW_get_address_Ajax_is_NOTok(self):
        """
            Verify if get address returns an ERROR if no address
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        data = {'id': 8, }
        data = json.dumps(data)
        response = self.c.post("/app_utilities/get_address/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"Error"' in response.content.decode('ascii')

    def test_VIEW_get_message_Ajax_is_NOTok(self):
        """
            Verify if get unknown message returns an error message
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        data = {'msg': 'dummymsg',}
        data = json.dumps(data)
        response = self.c.post("/app_utilities/get_message/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"Error -dummymsg- Not found!!!!"' in response.content.decode('ascii')

