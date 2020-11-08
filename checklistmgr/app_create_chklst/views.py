from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalReadView,
                                           BSModalUpdateView,
                                           BSModalDeleteView)
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from sortable_listview import SortableListView

from app_create_chklst.forms import CategoryModelForm, LineModelForm, CheckListCreateForm
from app_create_chklst.models import (Category,
                                      Line)

"""
All the modal view are from the BSModalview : https://github.com/trco/django-bootstrap-modal-forms
"""

class CategoryCreateView(BSModalCreateView):
    """
    Create category --> modal create View
    """
    template_name = 'app_create_chklst/dialogboxes/createcategory.html'
    form_class = CategoryModelForm
    form = CategoryModelForm
    success_message = 'CreatecatOK'
    success_url = reverse_lazy('app_create_chklst:chk-catmgmt')


class LineCreateView(BSModalCreateView):
    """
    Create line --> modal create View
    """
    template_name = 'app_create_chklst/dialogboxes/createline.html'
    form_class = LineModelForm
    form = LineModelForm
    success_message = 'LineCreateOK'
    success_url = reverse_lazy('app_create_chklst:chk-linemgmt')


class CategoryUpdateView(BSModalUpdateView):
    """
    Update category --> modal update view
    """
    model = Category
    template_name = 'app_create_chklst/dialogboxes/updatecategory.html'
    form_class = CategoryModelForm
    success_message = 'UpdatecatOK'
    success_url = reverse_lazy('app_create_chklst:chk-catmgmt')


class LineUpdateView(BSModalUpdateView):
    """
    Line update --> modal update view
    """
    model = Line
    template_name = 'app_create_chklst/dialogboxes/updateline.html'
    form_class = LineModelForm
    success_message = 'LineUpdateOK'
    success_url = reverse_lazy('app_create_chklst:chk-linemgmt')


class CategoryDeleteView(BSModalDeleteView):
    """
    Category Delete --> modal create view
    """
    template_name = 'app_create_chklst/dialogboxes/deletecategory.html'
    model = Category
    success_message = 'DeletecatOK'
    success_url = reverse_lazy('app_create_chklst:chk-catmgmt')

    def post(self, request, pk):
        category = Category.objects.get(pk=pk)
        if category.clc_categories.all().exists():
            messages.error(request, "Errdelcatchild")
        else:
            category.delete()
            messages.success(request, self.success_message)
        return redirect(self.success_url)


class LineDeleteView(BSModalDeleteView):
    """
    Line delete --> modal delete view
    """
    template_name = 'app_create_chklst/dialogboxes/deleteline.html'
    model = Line
    success_message = 'LineDeleteOK'
    success_url = reverse_lazy('app_create_chklst:chk-linemgmt')

    def post(self, request, pk):
        line = Line.objects.get(pk=pk)
        if line.cll_lines.all().exists():
            messages.error(request, "Errdellinechild")
        else:
            line.delete()
            messages.success(request, self.success_message)
        return redirect(self.success_url)


class CategoryDisplayView(BSModalReadView):
    """
    Category display --> modal display/read view
    """
    model = Category
    template_name = 'app_create_chklst/dialogboxes/displaycategory.html'


class LineDisplayView(BSModalReadView):
    """
    Line display --> modal display/read view
    """
    model = Line
    template_name = 'app_create_chklst/dialogboxes/displayline.html'


def CatandLineMgmtView(request):
    """
    display page with 2 tables : Categories & lines
    Context has 2 querysets (lines and categories) and parameters is for the 2 paginators
    if POST --> render the page
    if GET -->
        --> find if an error message and find for what (line or cat)
        --> get the querysets
        --> paginate
        --> render the page
    The whole CRUD for cat and lines are in the table.
    :param request:
    :return: render
    """
    context = {'title': "app_create_chklst_catlinemgmt_title"}
    if request.method == 'POST':
        return render(request, 'app_create_chklst/catandlinemgmt.html', context=context)
    if request.method == 'GET':
        list(messages.get_messages(request))
        if error := request.GET.get('error', None, ):
            if error[0:4] == 'Line':
                context['line_error'] = error
            else:
                context['error'] = error
        if message := request.GET.get('message', None, ):
            if message[0:4] == 'Line':
                context['line_message'] = message
            else:
                context['message'] = message
        # get Categories & lines
        if request.user.is_superuser:
            categories = Category.objects.all()
            lines = Line.objects.all()
        else:
            categories = Category.objects.filter(Q(cat_company=request.user.user_company))
            lines = Line.objects.filter(Q(line_company=request.user.user_company))
        # Cat paginator
        cat_page = request.GET.get('catpage', 1, )
        cat_paginator = Paginator(categories, 5)
        try:
            cat_users = cat_paginator.page(cat_page)
        except PageNotAnInteger:
            cat_users = cat_paginator.page(1)
        except EmptyPage:
            cat_users = cat_paginator.page(cat_paginator.num_pages)

        # Lines paginator

        line_page = request.GET.get('linepage', 1, )
        line_paginator = Paginator(lines, 5)
        try:
            line_users = line_paginator.page(line_page)
        except PageNotAnInteger:
            line_users = line_paginator.page(1)
        except EmptyPage:
            line_users = line_paginator.page(line_paginator.num_pages)

        context['categories'] = categories
        context['cat_users'] = cat_users
        context['line_users'] = line_users
        context['cur_page_cat'] = cat_page
        context['cur_page_line'] = line_page
        return render(request, 'app_create_chklst/catandlinemgmt.html', context=context)


class CategoryMgmtView(SortableListView):
    """
    Sortable list view of categories
    """
    context = {'title': 'Categories'}
    template_name = "app_create_chklst/categorymgmt.html"
    context_object_name = "cat_users"
    allowed_sort_fields = {"cat_key": {'default_direction': '', 'verbose_name': 'Key'},
                           "cat_wording": {'default_direction': '', 'verbose_name': 'Wording'},
                           "cat_enable": {'default_direction': '', 'verbose_name': 'Enable'},}
    default_sort_field = 'cat_key'  # mandatory
    paginate_by = 15

    def get_queryset(self):
        order = self.request.GET.get('sort', 'cat_key')

        if self.request.user.is_superuser:
            return Category.objects.all().order_by(order)
        else:
            return Category.objects.filter(Q(cat_company=self.request.user.user_company)).order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'cat_key')
        context['title'] = 'Categories'
        return context


class LineMgmtView(SortableListView):
    """
        Sortable list view of categories
    """
    context = {'title': 'Lines'}
    template_name = "app_create_chklst/linemgmt.html"
    context_object_name = "line_users"
    allowed_sort_fields = {"line_key": {'default_direction': '', 'verbose_name': 'Key'},
                           "line_wording": {'default_direction': '', 'verbose_name': 'Wording'},
                           "line_enable": {'default_direction': '', 'verbose_name': 'Enable'},
                           "line_type": {'default_direction': '', 'verbose_name': 'Type'},}
    default_sort_field = 'line_key'  # mandatory
    paginate_by = 10

    def get_queryset(self):
        order = self.request.GET.get('sort', 'line_key')

        if self.request.user.is_superuser:
            return Line.objects.all().order_by(order)
        else:
            return Line.objects.filter(Q(line_company=self.request.user.user_company)).order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'line_key')
        context['title'] = 'Lines'
        return context

