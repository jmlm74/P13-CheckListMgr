import inspect
import json

from django.test import Client, TransactionTestCase, RequestFactory
from django.urls import reverse, resolve

from app_checklist.forms import ChekListInput1Form, ChekListInput2Form, ChekListInput3Form, ChekListInput4Form
from app_checklist.models import CheckListDone
from app_checklist.saveviews import ChekListInput4
from app_checklist.views import ChekListInput1, ChekListInput2, ChekListInput3
from app_create_chklst.models import CheckList
from app_input_chklst.models import Material, Manager
from app_user.models import User, Company


class TestCheckList(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = Client()

    def setUp(self):
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        self.my_company = Company(company_name='toto')
        self.my_company.save()
        self.my_manager = Manager(mgr_name='mymanager', mgr_company=self.my_company)
        self.my_manager.save()
        self.my_material = Material(mat_designation="titi",
                                    mat_registration='Libellé',
                                    mat_type="zzz",
                                    mat_model="aaa",
                                    mat_enable=True,
                                    mat_company=self.my_company,
                                    mat_manager=self.my_manager, )
        self.my_material.save()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_URL_saisie1_is_ok(self):
        """
            test reverse and resolve for saisie1
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:saisie1')
        assert path == '/app_checklist/saisie1/'
        assert resolve(path).view_name == 'app_checklist:saisie1'

    def test_URL_saisie1_withparam_is_ok(self):
        """
            test reverse and resolve for saisie1 with a parameter
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:saisie1', args=[5])
        assert path == '/app_checklist/saisie1/5'
        assert resolve(path).view_name == 'app_checklist:saisie1'

    def test_URL_saisie2_is_ok(self):
        """
            test reverse and resolve for saisie2
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:saisie2')
        assert path == '/app_checklist/saisie2/'
        assert resolve(path).view_name == 'app_checklist:saisie2'

    def test_URL_saisie3_is_ok(self):
        """
            test reverse and resolve for saisie3
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:saisie3')
        assert path == '/app_checklist/saisie3/'
        assert resolve(path).view_name == 'app_checklist:saisie3'

    def test_URL_saisie3_priv_is_ok(self):
        """
            test reverse and resolve for saisie3-priv
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:saisie3-priv', args=[5])
        assert path == '/app_checklist/saisie3-priv/5'
        assert resolve(path).view_name == 'app_checklist:saisie3-priv'

    def test_URL_saisie4_is_ok(self):
        """
            test reverse and resolve for saisie4
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:saisie4')
        assert path == '/app_checklist/saisie4/'
        assert resolve(path).view_name == 'app_checklist:saisie4'

    def test_URL_ajax_getmanager_is_ok(self):
        """
            test reverse and resolve for getmanager
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:getmanager')
        assert path == '/app_checklist/getmanager/'
        assert resolve(path).view_name == 'app_checklist:getmanager'

    def test_URL_ajax_getmaterial_is_ok(self):
        """
            test reverse and resolve for getmaterial
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:getmaterial')
        assert path == '/app_checklist/getmaterial/'
        assert resolve(path).view_name == 'app_checklist:getmaterial'

    def test_URL_ajax_beforepreview_is_ok(self):
        """
            test reverse and resolve for beforepreview
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:beforepreview')
        assert path == '/app_checklist/beforepreview/'
        assert resolve(path).view_name == 'app_checklist:beforepreview'

    def test_URL_ajax_upload_photos_is_ok(self):
        """
            test reverse and resolve for upload_photos
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:upload_photos')
        assert path == '/app_checklist/upload_photos/'
        assert resolve(path).view_name == 'app_checklist:upload_photos'

    def test_URL_ajax_remove_photos_is_ok(self):
        """
            test reverse and resolve for remove_photos
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:remove_photos')
        assert path == '/app_checklist/remove_photos/'
        assert resolve(path).view_name == 'app_checklist:remove_photos'

    def test_URL_pdf_is_ok(self):
        """
            test reverse and resolve for pdf
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:pdf')
        assert path == '/app_checklist/pdf/'
        assert resolve(path).view_name == 'app_checklist:pdf'

    def test_URL_pdf_withparam_is_ok(self):
        """
            test reverse and resolve for pdf with parameter
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_checklist:pdf', args=['1'])
        assert path == '/app_checklist/pdf/1/'
        assert resolve(path).view_name == 'app_checklist:pdf'

    def test_FORM_ChekListInput1Form_isvalid(self):
        """
        verify the create ChekListInput1Form form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = ChekListInput1Form(data={
            'mat_designation': self.my_material,
            'mat_registration': 'titi',
            'mat_type': 'type',
            'mat_model': 'model',
            'mat_material': '',
            'mat_manager': self.my_manager
        })
        assert (form.is_valid())

    def test_FORM_ChekListInput1Form_isNOTvalid(self):
        """
        verify the create ChekListInput1Form form is not valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = ChekListInput1Form(data={
            'mat_designation': self.my_company,
            'mat_registration': 'titi',
            'mat_type': 'type',
            'mat_model': 'model',
            'mat_material': '',
            'mat_manager': self.my_manager
        })
        assert not (form.is_valid())

    def test_FORM_ChekListInput2Form_isvalid(self):
        """
        verify the create ChekListInput2Form form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = ChekListInput2Form(data={
            'mgr_name': self.my_manager,
            'mgr_contact': 'contact',
            'mgr_phone': '12345678',
            'mgr_email1': 'toto@tutu.fr',
            'mgr_email2': '',
            'mgr_id': 0
        })
        assert (form.is_valid())

    def test_FORM_ChekListInput2Form_isNOTvalid(self):
        """
        verify the create ChekListInput2Form form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = ChekListInput2Form(data={
            'mgr_name': self.my_manager,
            'mgr_contact': 'contact',
            'mgr_phone': '12345678',
            'mgr_email1': 'toto@tutu.fr',
            'mgr_email2': 'titi',
            'mgr_id': 0
        })
        assert not (form.is_valid())

    def test_FORM_ChekListInput3Form_isvalid(self):
        """
        verify the create ChekListInput3Form form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = ChekListInput3Form(data={
            'chk_title': 'title',
            'chk_save': 'contact',
            'chk_remsave': '12345678',
        })
        assert (form.is_valid())

    def test_FORM_ChekListInput4Form_isvalid(self):
        """
        verify the create ChekListInput4Form form is valid
        """
        print(inspect.currentframe().f_code.co_name)
        form = ChekListInput4Form(data={
            'cld_key': 'toto',
            'cld_valid': 'toto',
            'cld_remarks': '12345678',
            'cld_fotosave': "toto"
        })
        assert (form.is_valid())

    def test_VIEW_getmanager_Ajax_is_ok(self):
        """
            Verify if get manager return a manager and an OK response
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        data = {'id': self.my_manager.id, }
        data = json.dumps(data)
        response = self.c.post("/app_checklist/getmanager/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"OK"' in response.content.decode('ascii')
        assert '"mymanager"' in response.content.decode('ascii')

    def test_VIEW_getmaterial_Ajax_is_ok(self):
        """
            Verify if get material return a material and an OK response
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        data = {'id': self.my_material.id, }
        data = json.dumps(data)
        response = self.c.post("/app_checklist/getmaterial/", data, content_type="application/json")
        assert response.status_code == 200
        assert '"OK"' in response.content.decode('ascii')
        assert '"titi"' in response.content.decode('ascii')


class TestCheckListInput(TransactionTestCase):
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
                                      chk_enable=True, )
        self.my_checklist.save()
        self.user = User.objects.create_user(username='testuser2',
                                             password='toto',
                                             admin=True,
                                             user_company=self.my_company,
                                             email="toto@tutu.fr")
        self.new_checklist = CheckListDone.objects.create(cld_user=self.user,
                                                          cld_key="1",
                                                          cld_valid=True)
        self.my_manager = Manager.objects.create(mgr_name='mymanager', mgr_company=self.my_company,
                                                 mgr_email1='toto@tutu.com')

    def test_VIEW_ChekListInput1View_isOK(self):
        """
        verify view ChekListInput1 - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = ChekListInput1()
        view.setup(request)
        request.session = self.c.session
        request.user = self.user
        request.session['checklist_id'] = self.my_checklist.id
        request.session.save()
        context = view.get(request, pk=self.my_checklist.id)
        assert context.status_code == 200
        assert view.template_name == 'app_checklist/checklist_mat.html'


    def test_VIEW_ChekListInput1_is_OK(self):
        """
          Verify view checklistinput1 (post) --> must redirect to checklistinput2
          Just need a client session
        """
        print(inspect.currentframe().f_code.co_name)
        self.c.force_login(User.objects.get_or_create(username='testuser')[0])
        session = self.c.session
        session['checklist_id'] = self.my_checklist.id
        data = {'material': ''}
        response = self.c.post("/app_checklist/saisie1/", data)
        assert response.status_code == 302
        assert response.url == '/app_checklist/saisie2/'

    def test_VIEW_ChekListInput2View_isOK(self):
        """
        verify view ChekListInput2 - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = ChekListInput2()
        view.setup(request)
        request.session = self.c.session
        request.user = self.user
        request.session['checklist_id'] = self.my_checklist.id
        request.session['mat'] = {'manager': ""}
        request.session.save()
        context = view.get(request, pk=self.my_checklist.id)
        assert context.status_code == 200
        assert view.template_name == 'app_checklist/checklist_man.html'

    def test_VIEW_ChekListInput2_is_OK(self):
        """
          Verify view checklistinput2 (post) --> must redirect to checklistinput3
          Need a request session --> built with requestfactory
        """
        print(inspect.currentframe().f_code.co_name)
        factory = RequestFactory()
        request = factory.get('/app_checklist/saisie2/')
        request.session = self.c.session
        request.session['checklist_id'] = self.my_checklist.id
        request.session['mat'] = {'manager': ""}
        request.user = self.user
        request.session.save()
        data = {'manager': ''}
        response = self.c.post("/app_checklist/saisie2/", data)
        assert 302 == response.status_code
        assert response.url == '/app_checklist/saisie3/'

    def test_VIEW_ChekListInput3View_isOK(self):
        """
        verify view ChekListInput3 - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = ChekListInput3()
        view.setup(request)
        request.session = self.c.session
        request.user = self.user
        request.session['checklist_id'] = self.my_checklist.id
        request.session['mat'] = {'manager': "", 'mat': ""}
        request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert view.template_name == 'app_checklist/checklist_chklst.html'

    def test_VIEW_ChekListInput3_is_OK(self):
        """
          Verify view checklistinput3 (post) --> must redirect to checklistinput4
          Need a request session --> built with requestfactory
          test if checklist has been created in database
        """
        print(inspect.currentframe().f_code.co_name)
        factory = RequestFactory()
        request = factory.get('/app_checklist/saisie3/')
        request.session = self.c.session
        request.session['checklist_id'] = self.my_checklist.id
        request.session['mat'] = {'manager': "", 'mat': '0'}
        request.session['chklst'] = 0
        request.user = self.user
        request.session.save()
        data = {'chk_save': '', 'chk_remsave': ''}
        response = self.c.post("/app_checklist/saisie3/", data)
        assert 302 == response.status_code
        assert response.url == '/app_checklist/saisie4/'

    def test_VIEW_ChekListInput4View_isOK(self):
        """
        verify view ChekListInput4 - get
        """
        print(inspect.currentframe().f_code.co_name)
        request = RequestFactory().get('/')
        view = ChekListInput4()
        view.setup(request)
        request.session = self.c.session
        request.user = self.user
        request.session['checklist_id'] = self.my_checklist.id
        request.session['mat'] = {'manager': "", 'mat': ""}
        request.session['newchecklist_id'] = self.new_checklist.id
        request.session.save()
        context = view.get(request)
        assert context.status_code == 200
        assert view.template_name == 'app_checklist/checklist_finale.html'

    def test_VIEW_ChekListInput4_is_OK(self):
        """
          Verify view checklistinput4 (post) --> must redirect to checklistinput4
          Need a request session --> built with requestfactory
        """
        print(inspect.currentframe().f_code.co_name)
        nb1 = CheckListDone.objects.filter(cld_status=1).count()
        factory = RequestFactory()
        request = factory.get('/app_checklist/saisie4/')
        request.session = self.c.session
        request.session['checklist_id'] = self.my_checklist.id
        request.session['mat'] = {'manager': "", 'id': '0'}
        request.session['mgr'] = {'id': self.my_manager.id}
        request.session['chklst'] = 0
        request.session['newchecklist_id'] = self.new_checklist.id
        request.user = self.user
        request.session.save()
        data = {'cld_key': '1', 'cld_valid': 'on', 'cld_remarks': ''}
        response = self.c.post("/app_checklist/saisie4/", data)
        nb2 = CheckListDone.objects.filter(cld_status=1).count()
        assert 302 == response.status_code
        assert nb2 == nb1 + 1
        assert response.url == '/app_checklist/pdf/1/'

    def test_VIEW_before_preview(self):
        print(inspect.currentframe().f_code.co_name)
        factory = RequestFactory()
        request = factory.get('/')
        request.session = self.c.session
        data = {'cld_key': '111',
                'cld_valid': 'on',
                'cld_remarks': "totototo", }
        request.session['checklist_id'] = self.my_checklist.id
        request.session['mat'] = {'manager': "", 'id': '0'}
        request.session['mgr'] = {'id': self.my_manager.id}
        request.session['chklst'] = 0
        request.session['newchecklist_id'] = self.new_checklist.id
        request.user = self.user
        request.session.save()
        request.data = {'cld_key': '1', 'cld_valid': 'on', 'cld_remarks': ''}
        data = json.dumps(data)
        response = self.c.post("/app_checklist/beforepreview/",
                               data,
                               content_type="application/json",
                               **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        assert response.status_code == 200
        assert "OK" in response.content.decode('ascii')


