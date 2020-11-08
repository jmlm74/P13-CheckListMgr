import json

from django.contrib.auth import authenticate, login
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from sortable_listview import SortableListView

from app_checklist.models import CheckListDone
from app_create_chklst.models import CheckList
from app_input_chklst.models import Material, Manager
from app_user.forms import UserCheckListMgrFormLogin


class Index(View):
    """
    Home page view --> Login form + geolocalisation (js) + weather report (js)
    """
    context = {'title': "app_user-home-title"}
    template_name = 'app_home/home.html'
    form = UserCheckListMgrFormLogin

    def get(self, request):
        try:
            request.session['language']
        except KeyError:
            request.session['language'] = 'UK'
        self.context['form'] = self.form(None)
        return render(request, self.template_name, context=self.context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            bot = request.POST['bot_catcher']
            if len(bot):
                print("BOT-CATCHER !!!")  # Bot cather to use later with fail2ban ie
                self.context['form'] = self.form
                return render(request, 'bot-catcher.html')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    print(f"Connection of {username}")  # for the logs
                    request.session['language'] = str(user.preferred_language)
                    return HttpResponseRedirect(reverse('app_home:main'))  # return to the index
                else:
                    form.add_error(None, "Userdisabled")
            else:
                # a message to be used with fail2ban later
                print(f"Someone try to login and failed ! user : {username} - psw : {password}")
                form.add_error(None, "Userpswinvalid")
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('app_home:main'))
        self.context['form'] = form
        return render(request, self.template_name, context=self.context)


class LegalView(TemplateView):
    """
    display legal
    """
    template_name = "app_home/legal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Legal'
        return context


class ContactView(TemplateView):
    """
    display contact view
    """
    template_name = "app_home/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact'
        return context


class MainView(SortableListView):
    """
    The main view
    2 steps : The sortable list of the checklist you can input
            : The list of the checklist already input (limit 15)
    The sortable list is set in the def_queryset
    The check-lists are obtained in the get context data
    """
    context = {'title': 'Main'}
    template_name = "app_home/main.html"
    context_object_name = "checklists"
    allowed_sort_fields = {"chk_key": {'default_direction': '', 'verbose_name': 'Key'},
                           "chk_title": {'default_direction': '', 'verbose_name': 'Wording'},
                           }
    default_sort_field = 'chk_key'  # mandatory
    paginate_by = 5

    def get_queryset(self):
        order = self.request.GET.get('sort', 'chk_key')
        if self.request.user.is_superuser:
            return CheckList.objects.all().order_by(order)
        else:
            return CheckList.objects.filter(Q(chk_company=self.request.user.user_company)).order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'chk_key')
        context['title'] = 'Main'
        if self.request.user.is_superuser:
            checklistsdone = CheckListDone.objects.filter(cld_status=1).order_by('-modified_date')[:20]
        else:
            checklistsdone = CheckListDone.objects.filter(cld_company=self.request.user.user_company).\
            filter(cld_status=1).order_by('-modified_date')[:20]
        context['checklistsdone'] = checklistsdone
        return context


def autocomplete_search_mat(request):
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        manager = request_data['manager']
        if request.user.is_superuser:
            query = Q()
        else:
            query = Q(mat_company=request.user.user_company)
        if manager != '':
            query &= Q(mat_manager_id=manager)
        materials = Material.objects.filter(query).order_by("mat_designation")
        data = serializers.serialize('json', materials)
    return HttpResponse(data)


def autocomplete_search_man(request):
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        material = request_data['material']
        if request.user.is_superuser:
            query = Q()
        else:
            query = Q(mgr_company=request.user.user_company)
        if material != '' and material != '0':
            query &= Q(mat_manager__id=material)
        manager = Manager.objects.filter(query).order_by("mgr_name")
        data = serializers.serialize('json', manager)
    return HttpResponse(data)


def search_chklst(request):
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        query = Q(cld_status=1)
        if not request.user.is_superuser:
            query &= Q(cld_company=request.user.user_company)
        if 'material' in request_data:
            query &= Q(cld_material_id=request_data['material'])
        if 'manager' in request_data:
            query &= Q(cld_manager_id=request_data['manager'])
        if 'date' in request_data:
            query &= Q(modified_date__icontains=request_data['date'])
        checklists_done = CheckListDone.objects.filter(query).order_by('-modified_date')[:20]
        data = []
        for idx, chklst in enumerate(checklists_done):
            data.append({'key': chklst.cld_key,
                         'valid': chklst.cld_valid,
                         'pdf': chklst.cld_pdf_file.url,
                         'date': str(chklst.modified_date)[:10],
                         'title': chklst.cld_checklist.chk_title[:30],
                         })
            try:
                data[idx]['manager'] = chklst.cld_manager.mgr_name
            except AttributeError:
                data[idx]['manager'] = ''
            try:
                data[idx]['material'] = chklst.cld_material.mat_designation
            except AttributeError:
                data[idx]['material'] = ''
            if request.user.is_superuser:
                data[idx]['company'] = chklst.cld_company.company_name
        data = json.dumps(data)
    return HttpResponse(data)
