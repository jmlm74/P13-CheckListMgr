from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalUpdateView, BSModalDeleteView

from django.contrib import messages
from django.db.models import RestrictedError
from django.shortcuts import redirect
from django.urls import reverse_lazy

from app_input_chklst.forms import MaterialCreateForm
from app_input_chklst.models import Manager, Material


class MaterialCreateView(BSModalCreateView):
    """
    Create manager --> modal create View
    """
    template_name = 'app_input_chklst/dialogboxes/creatematerial.html'
    form_class = MaterialCreateForm
    form = MaterialCreateForm
    success_message = 'CreatematOK'
    success_url = reverse_lazy('app_input_chklst:inp-main')

    def get_success_url(self):
        url = self.request.GET.get('url', None)
        if url:
            return url
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(MaterialCreateView, self).get_context_data(**kwargs)
        # print(kwargs)

        context['title'] = "Createmat"
        context['btn'] = "Create"
        context['form'].fields['mat_manager'].queryset = Manager.objects.\
            filter(mgr_company=self.request.user.user_company)
        context['form'].fields['mat_material'].queryset = Material.objects. \
            filter(mat_company=self.request.user.user_company)
        return context


class MaterialDisplayView(BSModalReadView):
    """
    Manager display --> modal display/read view
    """
    model = Material
    template_name = 'app_input_chklst/dialogboxes/displaymaterial.html'
    # mat2 = Material.objects.filter(mat_secondary__mat_material=mat)




    def get_context_data(self, **kwargs):
        context = super(MaterialDisplayView, self).get_context_data(**kwargs)
        material = Material.objects.get(pk=self.kwargs['pk'])
        mat2nd = Material.objects.filter(mat_material=material)
        if mat2nd.count() > 0:
            context['mat2nd'] = mat2nd
        context['title'] = "Displaymat"
        return context


class MaterialUpdateView(BSModalUpdateView):
    """
    Update manager --> modal update view
    """
    model = Material
    template_name = 'app_input_chklst/dialogboxes/creatematerial.html'
    form_class = MaterialCreateForm
    success_message = 'UpdatematOK'
    success_url = reverse_lazy('app_input_chklst:inp-main')

    def get_context_data(self, **kwargs):
        context = super(MaterialUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Updatemat"
        context['btn'] = "Update"
        return context


class MaterialDeleteView(BSModalDeleteView):
    """
    Manager Delete --> modal delete view
    """
    template_name = 'app_input_chklst/dialogboxes/deletemat.html'
    model = Material
    success_message = 'DeletematOK'
    error_message = 'DeletematKO'
    success_url = reverse_lazy('app_input_chklst:inp-main')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
        except RestrictedError:
            messages.error(request, self.error_message)
        return redirect(self.success_url)

