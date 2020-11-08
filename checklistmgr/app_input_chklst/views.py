from django.db.models import Q

from sortable_listview import SortableListView

from app_input_chklst.models import Material


class MainInputView(SortableListView):
    """
    List materials --> sortable list view
    """
    context = {'title': 'Materials'}
    template_name = "app_input_chklst/maininput.html"
    context_object_name = "materials"
    allowed_sort_fields = {"mat_designation": {'default_direction': '', 'verbose_name': 'Designation'},
                           "mat_registration": {'default_direction': '', 'verbose_name': 'Serial/N'},
                           "mat_type": {'default_direction': '', 'verbose_name': 'Type'},
                           "mat_model": {'default_direction': '', 'verbose_name': 'Model'},
                           "mat_enable": {'default_direction': '', 'verbose_name': 'Enable'},
                           "mat_manager": {'default_direction': '', 'verbose_name': 'Manager'},
                           "mat_material": {'default_direction': '', 'verbose_name': 'Materialprim'}, }
    default_sort_field = 'mat_designation'  # mandatory
    paginate_by = 5

    def get_queryset(self):
        order = self.request.GET.get('sort', 'mat_designation')
        if self.request.user.is_superuser:
            return Material.objects.all().order_by(order)
        else:
            return Material.objects.filter(Q(mat_company=self.request.user.user_company)).order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'mat_designation')
        context['title'] = 'Materials'
        return context
