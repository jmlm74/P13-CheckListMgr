from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalUpdateView, BSModalDeleteView
from sortable_listview import SortableListView

from django.contrib import messages
from django.db.models import Q, RestrictedError
from django.shortcuts import redirect
from django.urls import reverse_lazy

from app_input_chklst.forms import ManagerCreateForm
from app_input_chklst.models import Manager


class MgrMgmtView(SortableListView):
    """
    List managers --> list sortable
    """
    context = {'title': 'Managers'}
    template_name = "app_input_chklst/managermgmt.html"
    context_object_name = "managers"
    allowed_sort_fields = {"mgr_name": {'default_direction': '', 'verbose_name': 'Manager'},
                           "mgr_contact": {'default_direction': '', 'verbose_name': 'Contactname'},
                           "mgr_phone": {'default_direction': '', 'verbose_name': 'Phone'},
                           "mgr_email1": {'default_direction': '', 'verbose_name': 'Email1'},
                           "mgr_email2": {'default_direction': '', 'verbose_name': 'Email2'},
                           "mgr_enable": {'default_direction': '', 'verbose_name': 'Enable'}, }
    default_sort_field = 'mgr_name'  # mandatory
    paginate_by = 5

    def get_queryset(self):
        order = self.request.GET.get('sort', 'mgr_name')

        if self.request.user.is_superuser:
            return Manager.objects.all().order_by(order)
        else:
            return Manager.objects.filter(Q(mgr_company=self.request.user.user_company)).order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'mgr_name')
        context['title'] = 'Managers'
        return context


class ManagerCreateView(BSModalCreateView):
    """
    Create manager --> modal create View
    """
    template_name = 'app_input_chklst/dialogboxes/createmanager.html'
    form_class = ManagerCreateForm
    form = ManagerCreateForm
    success_message = 'CreatemgrOK'
    success_url = reverse_lazy('app_input_chklst:inp-mgrmgmt')

    def get_success_url(self):
        url = self.request.GET.get('url', None)
        if url:
            return url
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(ManagerCreateView, self).get_context_data(**kwargs)
        context['title'] = "Createmgr"
        context['btn'] = "Create"
        return context


class ManagerDisplayView(BSModalReadView):
    """
    Manager display --> modal display/read view
    """
    model = Manager
    template_name = 'app_input_chklst/dialogboxes/displaymanager.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerDisplayView, self).get_context_data(**kwargs)
        context['title'] = "Displaymgr"
        return context


class ManagerUpdateView(BSModalUpdateView):
    """
    Update manager --> modal update view
    """
    model = Manager
    template_name = 'app_input_chklst/dialogboxes/createmanager.html'
    form_class = ManagerCreateForm
    success_message = 'UpdatemgrOK'
    success_url = reverse_lazy('app_input_chklst:inp-mgrmgmt')

    def get_context_data(self, **kwargs):
        context = super(ManagerUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Updatemgr"
        context['btn'] = "Update"
        return context


class ManagerDeleteView(BSModalDeleteView):
    """
    Manager Delete --> modal delete view
    """
    template_name = 'app_input_chklst/dialogboxes/deletemgr.html'
    model = Manager
    success_message = 'DeletemgrOK'
    error_message = 'DeletemgrKO'
    success_url = reverse_lazy('app_input_chklst:inp-mgrmgmt')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
        except RestrictedError:
            messages.error(request, self.error_message)
        return redirect(self.success_url)
