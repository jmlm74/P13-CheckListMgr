from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalUpdateView, BSModalDeleteView
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


from app_create_chklst.models import Category, Line
from app_create_chklst.forms import CategoryModelForm, LineModelForm


class CategoryCreateView(BSModalCreateView):
    template_name = 'app_create_chklst/dialogboxes/createcategory.html'
    form_class = CategoryModelForm
    form = CategoryModelForm
    success_message = 'CreatecatOK'
    success_url = reverse_lazy('app_create_chklst:catlineMgmt')


class LineCreateView(BSModalCreateView):
    template_name = 'app_create_chklst/dialogboxes/createline.html'
    form_class = LineModelForm
    form = LineModelForm
    success_message = 'LineCreateOK'
    success_url = reverse_lazy('app_create_chklst:catlineMgmt')


class CategoryUpdateView(BSModalUpdateView):
    model = Category
    template_name = 'app_create_chklst/dialogboxes/updatecategory.html'
    form_class = CategoryModelForm
    success_message = 'UpdatecatOK'
    success_url = reverse_lazy('app_create_chklst:catlineMgmt')


class LineUpdateView(BSModalUpdateView):
    model = Line
    template_name = 'app_create_chklst/dialogboxes/updateline.html'
    form_class = LineModelForm
    success_message = 'LineUpdateOK'
    success_url = reverse_lazy('app_create_chklst:catlineMgmt')

class CategoryDeleteView(BSModalDeleteView):
    template_name = 'app_create_chklst/dialogboxes/deletecategory.html'
    model = Category
    success_message = 'DeletecatOK'
    success_url = reverse_lazy('app_create_chklst:catlineMgmt')


class LineDeleteView(BSModalDeleteView):
    template_name = 'app_create_chklst/dialogboxes/deleteline.html'
    model = Line
    success_message = 'LineDeleteOK'
    success_url = reverse_lazy('app_create_chklst:catlineMgmt')


class CategoryDisplayView(BSModalReadView):
    model = Category
    template_name = 'app_create_chklst/dialogboxes/displaycategory.html'

class LineDisplayView(BSModalReadView):
    model = Line
    template_name = 'app_create_chklst/dialogboxes/displayline.html'


def CatandLineMgmtView(request):
    context = {'title': "app_create_chklst_catlinemgmt_title"}
    if request.method == 'POST':
        return render(request, 'app_create_chklst/catandlinemgmt.html', context=context)
    if request.method == 'GET':
        list(messages.get_messages(request))
        if error := request.GET.get('error', None):
            if error[0:4] == 'Line':
                context['line_error'] = error
            else:
                context['error'] = error
        if message := request.GET.get('message', None):
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
        cat_page = request.GET.get('catpage', 1)
        cat_paginator = Paginator(categories, 5)
        try:
            cat_users = cat_paginator.page(cat_page)
        except PageNotAnInteger:
            cat_users = cat_paginator.page(1)
        except EmptyPage:
            cat_users = cat_paginator.page(cat_paginator.num_pages)

        # Lines paginator

        line_page = request.GET.get('linepage', 1)
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




