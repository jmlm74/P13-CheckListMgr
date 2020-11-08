import inspect

from django.test import Client, TransactionTestCase
from django.urls import reverse, resolve

from app_input_chklst.forms import MaterialCreateForm
from app_input_chklst.models import Manager, Material
from app_user.models import User, Company


class Testmaterials(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = Client()

    def setUp(self):
        self.my_company = Company(company_name='toto')
        self.my_company.save()
        self.my_manager = Manager(mgr_name='mymanager',mgr_company=self.my_company)
        self.my_manager.save()
        self.c.force_login(User.objects.get_or_create(username='testuser',user_company=self.my_company)[0])


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_URL_main_material_is_ok(self):
        """
            test reverse and resolve for main/material
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-main')
        assert path == '/app_input_chklst/maininput/'
        assert resolve(path).view_name == 'app_input_chklst:inp-main'

    def test_URL_delete_material_is_ok(self):
        """
            test reverse and resolve for remove material
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-matdelete', args=[5])
        assert path == '/app_input_chklst/materialdelete/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-matdelete'

    def test_URL_display_material_is_ok(self):
        """
            test reverse and resolve for display material
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-matdisplay', args=[5])
        assert path == '/app_input_chklst/materialdisplay/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-matdisplay'

    def test_URL_update_material_is_ok(self):
        """
            test reverse and resolve for update material
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_input_chklst:inp-matupdate', args=[5])
        assert path == '/app_input_chklst/materialupdate/5'
        assert resolve(path).view_name == 'app_input_chklst:inp-matupdate'

    def test_FORM_Creatematerial_isvalid(self):
        """
        verify the create material form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = MaterialCreateForm(data={
            'mat_designation': "toto",
            'mat_registration': 'Libellé',
            'mat_type': "zzz",
            'mat_model': "aaa",
            'mat_enable': True,
            'mat_company': self.my_company,
            'mat_manager': self.my_manager,
        })
        assert(form.is_valid())

    def test_FORM_Creatematerial_isNOTvalid(self):
        """
        verify the create material form is NOT valid --> invalid data
        """
        print(inspect.currentframe().f_code.co_name)
        form = MaterialCreateForm(data={
            'mat_designation': "toto",
            'mat_registration': 'Libellé',
            'mat_type': "zzz",
            'mat_model': "aaa",
            'mat_enable': True,
            'mat_company': self.my_company,
            'mat_manager': None,
        })
        assert not (form.is_valid())

    def test_VIEW_create_material_is_ok(self):
        """
            Verify checklist creation is OK --> RC = 302 + 1 more line in the table
        """
        print(inspect.currentframe().f_code.co_name)
        nb1 = Material.objects.all().count()
        data = {
            'mat_designation': "titi",
            'mat_registration': 'Libellé',
            'mat_type': "zzz",
            'mat_model': "aaa",
            'mat_enable': True,
            'mat_company': self.my_company.id,
            'mat_manager': self.my_manager.id,
        }
        response = self.c.post("/app_input_chklst/materialcreate/", data)
        nb2 = Material.objects.all().count()
        assert response.status_code == 302
        assert nb1 + 1 == nb2

    def test_VIEW_create_material_is_NOTok(self):
        """
            Verify material creation is NOT OK --> RC = 200 and same number of lines
        """
        print(inspect.currentframe().f_code.co_name)
        new_material = Material(mat_designation="titi",
                                mat_registration='Libellé',
                                mat_type="zzz",
                                mat_model="aaa",
                                mat_enable=True,
                                mat_company=self.my_company,
                                mat_manager=self.my_manager,)
        new_material.save()

        nb1 = Material.objects.all().count()
        data = {
            'mat_designation': "titi",
            'mat_registration': 'Libellé2',
            'mat_type': "zzz2",
            'mat_model': "aaa2",
            'mat_enable': True,
            'mat_company': self.my_company.id,
            'mat_manager': self.my_manager.id,
        }
        response = self.c.post("/app_input_chklst/materialcreate/", data)
        nb2 = Material.objects.all().count()
        assert response.status_code == 200
        assert nb1 == nb2

    def test_VIEW_update_material_is_ok(self):
        """
            Verify material update is OK --> RC = 302 + updated material
        """
        print(inspect.currentframe().f_code.co_name)
        new_material = Material(mat_designation="titi",
                                mat_registration='Libellé',
                                mat_type="zzz",
                                mat_model="aaa",
                                mat_enable=True,
                                mat_company=self.my_company,
                                mat_manager=self.my_manager,)
        new_material.save()
        data = {
            'mat_designation': "toto2",
            'mat_registration': 'Libellé2',
            'mat_type': "zzz2",
            'mat_model': "aaa2",
            'mat_enable': True,
            'mat_company': self.my_company.id,
            'mat_manager': self.my_manager.id,
        }
        response = self.c.post("/app_input_chklst/materialupdate/" + str(new_material.id), data)

        updated_material = Material.objects.get(mat_designation='toto2')
        assert response.status_code == 302
        assert updated_material.mat_designation == 'toto2'
