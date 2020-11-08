from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalUpdateView, BSModalDeleteView
from sortable_listview import SortableListView

from django.contrib import messages
from django.db.models import RestrictedError
from django.shortcuts import redirect
from django.urls import reverse_lazy

from app_input_chklst.forms import AddressCreateForm
from app_user.models import Address


class AddressMgmtView(SortableListView):
    context = {'title': 'Addresses'}
    template_name = "app_input_chklst/addressmgmt.html"
    context_object_name = "addresses"
    allowed_sort_fields = {"address_name": {'default_direction': '', 'verbose_name': 'Address'},
                           "zipcode": {'default_direction': '', 'verbose_name': 'Zipcode'}, }
    default_sort_field = 'address_name'  # mandatory
    paginate_by = 5

    def get_queryset(self):
        order = self.request.GET.get('sort', 'address_name')
        if self.request.user.is_superuser:
            return Address.objects.all().order_by(order)
        else:
            return Address.objects.all().order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'address_name')
        context['title'] = 'Addresses'
        return context


class AddressCreateView(BSModalCreateView):
    """
    Create manager --> modal View
    """
    template_name = 'app_input_chklst/dialogboxes/createaddress.html'
    form_class = AddressCreateForm
    form = AddressCreateForm
    success_message = 'CreateadrOK'
    success_url = reverse_lazy('app_input_chklst:inp-addrmgmt')

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        context['title'] = "Createaddr"
        context['btn'] = "Create"
        return context


class AddressUpdateView(BSModalUpdateView):
    """
    Update manager --> modal view
    """
    model = Address
    template_name = 'app_input_chklst/dialogboxes/createaddress.html'
    form_class = AddressCreateForm
    success_message = 'UpdateaddrOK'
    success_url = reverse_lazy('app_input_chklst:inp-addrmgmt')

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Updateaddr"
        context['btn'] = "Update"
        return context


class AddressDisplayView(BSModalReadView):
    """
    Manager display --> modal view
    """
    model = Address
    template_name = 'app_input_chklst/dialogboxes/displayaddress.html'

    def get_context_data(self, **kwargs):
        context = super(AddressDisplayView, self).get_context_data(**kwargs)
        context['title'] = "Displayaddr"
        return context


class AddressDeleteView(BSModalDeleteView):
    """
    Manager Delete --> modal view
    """
    template_name = 'app_input_chklst/dialogboxes/deleteaddr.html'
    model = Address
    success_message = 'DeleteaddrOK'
    error_message = "DeleteaddrKO"
    success_url = reverse_lazy('app_input_chklst:inp-addrmgmt')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
        except RestrictedError:
            messages.error(request, self.error_message)
        return redirect(self.success_url)

