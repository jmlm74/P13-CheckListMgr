import json
import os

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from app_checklist.forms import ChekListInput1Form, ChekListInput2Form, ChekListInput3Form
from app_checklist.models import CheckListDone
from app_input_chklst.models import Material, Manager
from app_create_chklst.models import CheckList

"""
All of the views above have the same principe to catch Next & Previous buttons.
The views are a workflow --> you enter e material then a manager then The Check-list, 
    finally the name... eventually preview the pdf file then save it en send it by mail.
                         --> in Each step you can go previous or next without loosing data
All the page datas are stored in session data (dicts - POST methods) to retrieve 
them when the page is reloaded (GET method)
"""
class ChekListInput1(View):
    """
    view for input material for a checklist
    """
    context = {'title': 'Material'}
    template_name = "app_checklist/checklist_mat.html"
    form = ChekListInput1Form
    context_object_name = 'material'

    def get(self, request, *args, **kwargs):
        # 1st load of 1st page --> remove all the context of the workflow
        if kwargs:
            if 'mat' in request.session:
                del request.session['mat']
            if 'mgr' in request.session:
                del request.session['mgr']
            if 'chklst' in request.session:
                del request.session['chklst']
            if 'chksave' in request.session:
                del request.session['chksave']
            if 'checklist_id' in request.session:
                del request.session['checklist_id']
            request.session.modified = True
            list(messages.get_messages(request))
            self.context['checklist_id'] = kwargs['pk']
            self.context['url'] = reverse('app_checklist:saisie1') + str(kwargs['pk'])
        self.context["materials"] = Material.objects.filter(mat_company=self.request.user.user_company).\
            filter(mat_enable=True).order_by('mat_designation')
        # first load of page
        if 'mat' not in request.session:
            request.session['checklist_id'] = kwargs['pk']
            request.session['mat'] = {}
            request.session['mat']['encours'] = 0
            self.context['form'] = self.form
            # find if a checklist is already in progress for user and catch the id or create a new one to get the id
            checklist_done = CheckListDone.objects.filter(cld_user=self.request.user).filter(cld_status=0)
            if checklist_done.count() == 0:
                new_checklist = CheckListDone.objects.create(cld_user=self.request.user)
            else:
                new_checklist = checklist_done[0]
                file = new_checklist.cld_pdf_file
                if file:
                    media_root = getattr(settings, 'MEDIA_ROOT', None)
                    try:
                        os.remove(os.path.join(media_root, str(file)))
                    except FileNotFoundError:
                        pass
                for photo in new_checklist.pho_chklst.all():
                    photo.delete()
            request.session['newchecklist_id'] = new_checklist.pk
        # not the first load --> get all the form values in session (dict mat) then load the form with them
        elif request.session['mat']['encours'] == 1:
            mat_registration = request.session['mat']['mat_registration']
            mat_model = request.session['mat']['mat_model']
            mat_type = request.session['mat']['mat_type']
            material = request.session['mat']['id']
            mat_material = request.session['mat']['material']
            mat_manager = request.session['mat']['manager']
            self.context['form'] = self.form(initial={'mat_registration': mat_registration,
                                                      'mat_model': mat_model,
                                                      'mat_type': mat_type,
                                                      'mat_id': material,
                                                      'mat_material': mat_material,
                                                      'mat_manager': mat_manager, })
        else:
            self.context['form'] = self.form
        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        # if valid --> store the form in session (dict mat)
        if form.is_valid():
            request.session['mat'] = {}
            request.session['mat']['encours'] = 1
            request.session['mat']['id'] = request.POST['material']  # id
            request.session['mat']['mat_registration'] = form.cleaned_data['mat_registration']
            request.session['mat']['mat_type'] = form.cleaned_data['mat_type']
            request.session['mat']['mat_model'] = form.cleaned_data['mat_model']
            request.session['mat']['material'] = form.cleaned_data['mat_material']
            request.session['mat']['manager'] = form.cleaned_data['mat_manager']
        return redirect('app_checklist:saisie2')


class ChekListInput2(View):
    """
    view for input manager of a checklist
    """
    context = {'title': 'Manager'}
    template_name = "app_checklist/checklist_man.html"
    form = ChekListInput2Form
    context_object_name = 'manager'

    def get(self, request, *args, **kwargs):
        list(messages.get_messages(request))
        self.context['url'] = reverse('app_checklist:saisie2')
        self.context["managers"] = Manager.objects.filter(mgr_company=self.request.user.user_company).\
            filter(mgr_enable=True)
        if 'mgr' not in request.session:
            # the 1st load of form
            request.session['mgr'] = {}
            request.session['mgr']['encours'] = 0
            # no material selected --> no manager to display
            if request.session['mat']['manager'] == '':
                self.context['form'] = self.form(None)
                return render(request, self.template_name, context=self.context)
            # material selected --> get material manager and display (load the initial form)
            manager = Manager.objects.get(pk=request.session['mat']['manager'])
            self.context['form'] = self.form(initial={'mgr_contact': manager.mgr_contact,
                                                      'mgr_phone': manager.mgr_phone,
                                                      'mgr_email1': manager.mgr_email1,
                                                      'mgr_email2': manager.mgr_email2,
                                                      'mgr_id': manager.pk,
                                                      'manager': manager.mgr_name, })
        elif request.session['mgr']['encours'] == 1:
            # not the 1st load --> load the form data in the session dict then display
            mgr_id = request.session['mgr']['id']
            mgr_contact = request.session['mgr']['mgr_contact']
            mgr_phone = request.session['mgr']['mgr_phone']
            mgr_email1 = request.session['mgr']['mgr_email1']
            mgr_email2 = request.session['mgr']['mgr_email2']
            self.context['form'] = self.form(initial={'mgr_contact': mgr_contact,
                                                      'mgr_phone': mgr_phone,
                                                      'mgr_email1': mgr_email1,
                                                      'mgr_email2': mgr_email2,
                                                      'mgr_id': mgr_id,
                                                      })
        else:
            self.context['form'] = self.form
        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        # print(request)
        form = self.form(request.POST)
        if form.is_valid():
            # valid --> save the form in session
            request.session['mgr'] = {}
            request.session['mgr']['id'] = request.POST['manager']  # id
            request.session['mgr']['mgr_contact'] = form.cleaned_data['mgr_contact']
            request.session['mgr']['mgr_phone'] = form.cleaned_data['mgr_phone']
            request.session['mgr']['mgr_email1'] = form.cleaned_data['mgr_email1']
            request.session['mgr']['mgr_email2'] = form.cleaned_data['mgr_email2']
            request.session['mat']['manager'] = request.POST['manager']
        # 2 submit buttons next & previous
        request.session['mgr']['encours'] = 1
        if 'previous' in request.POST:
            return redirect('app_checklist:saisie1')

        return redirect('app_checklist:saisie3')


class ChekListInput3(View):
    """
    view for input choices of a checklist (pro user)
    This one is only for pro users (material & manager data exist)
    It's more suitable to have 2 views (pro and priv)
    """
    context = {'title': 'Checklist'}
    template_name = "app_checklist/checklist_chklst.html"
    form = ChekListInput3Form
    context_object_name = 'Checklist'

    def get(self, request):
        checklist_id = request.session['checklist_id']
        checklist = CheckList.objects.get(pk=checklist_id)
        details = checklist.chklst_detail()
        self.context['checklist'] = checklist
        self.context['details'] = details
        # 1st load
        if 'chklst' not in request.session or request.session['chklst'] == 0:
            request.session['chklst'] = {}
            request.session['chklst'] = 0
            self.context['form'] = self.form
        else:
            chk_save = request.session['chklst']['save']
            chk_remsave = request.session['chklst']['remsave']
            self.context['form'] = self.form(initial={'chk_save': chk_save, 'chk_remsave': chk_remsave, })
        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            # valid --> save the form in session
            request.session['chklst'] = {}
            request.session['chklst']['save'] = request.POST['chk_save']  # save radiobuttons states
            request.session['chklst']['remsave'] = request.POST['chk_remsave']  # save remarks
            # print(request.POST['chk_remsave'])
        # 2 submit buttons next & previous
        if 'previous' in request.POST:
            return redirect('app_checklist:saisie2')
        return redirect('app_checklist:saisie4')


def cheklistinput3_priv(request, *args, **kwargs):
    """
    view for input choices of a checklist (private user)
    This one is only for priv users (material & manager data don't exist)
    """
    if 'mat' in request.session:
        del request.session['mat']
    if 'mgr' in request.session:
        del request.session['mgr']
    if 'chklst' in request.session:
        del request.session['chklst']
    if 'chksave' in request.session:
        del request.session['chksave']
    if 'checklist_id' in request.session:
        del request.session['checklist_id']
    request.session.modified = True
    list(messages.get_messages(request))
    request.session['checklist_id'] = kwargs['pk']
    request.session['mat'] = {'encours': '1',
                              'id': '0',
                              'manager': '0',
                              'mat_model': '',
                              'mat_registration': '',
                              'mat_type': '',
                              'material': ''}
    request.session['mgr'] = {'encours': '1',
                              'id': '0',
                              'mgr_contact': '',
                              'mgr_email1': '',
                              'mgr_email2': '',
                              'mgr_phone': ''}
    checklist_done = CheckListDone.objects.filter(cld_user=request.user).filter(cld_status=0)
    if checklist_done.count() == 0:
        new_checklist = CheckListDone.objects.create(cld_user=request.user)
    else:
        new_checklist = checklist_done[0]
        file = new_checklist.cld_pdf_file
        if file:
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            try:
                os.remove(os.path.join(media_root, str(file)))
            except FileNotFoundError:
                pass
        for photo in new_checklist.pho_chklst.all():
            photo.delete()
    request.session['newchecklist_id'] = new_checklist.pk
    return redirect('app_checklist:saisie3')


# Ajax
def getmanager(request):
    """
    get manager --> Input json datafile : id
                --> output json datafile : manager
    """
    if request.method == 'POST':
        data = {'data': 'ERROR'}
        request_data = json.loads(request.read().decode('utf-8'))
        man_id = request_data['id']
        manager = Manager.objects.get(pk=man_id)
        data['data'] = 'OK'
        data['mgr_name'] = manager.mgr_name
        data['mgr_contact'] = manager.mgr_contact
        data['mgr_phone'] = manager.mgr_phone
        data['mgr_email1'] = manager.mgr_email1
        data['mgr_email2'] = manager.mgr_email2
    return JsonResponse(data)


def getmaterial(request):
    """
    get material --> Input json datafile : id
                --> output json datafile : material
    """
    if request.method == 'POST':
        data = {'data': 'ERROR'}
        request_data = json.loads(request.read().decode('utf-8'))
        mat_id = request_data['id']
        material = Material.objects.get(pk=mat_id)
        data['data'] = 'OK'
        data['mat_designation'] = material.mat_designation
        data['mat_registration'] = material.mat_registration
        data['mat_type'] = material.mat_type
        data['mat_model'] = material.mat_model
        try:
            data['mat_manager'] = material.mat_manager.id
        except AttributeError:
            data['mat_manager'] = ''
        try:
            data['mat_material'] = material.mat_material.mat_designation
        except AttributeError:
            data['mat_material'] = ''
        # data = json.dumps(data)
    return JsonResponse(data)
