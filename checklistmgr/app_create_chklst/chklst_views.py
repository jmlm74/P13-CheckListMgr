import json

from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalReadView
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from app_create_chklst.forms import CheckListCreateForm
from app_create_chklst.models import (Category,
                                      CheckListLine,
                                      CheckListCategory,
                                      CheckList,
                                      Line)
from app_user.models import Company


class ChklstDeleteView(BSModalDeleteView):
    template_name = 'app_create_chklst/dialogboxes/deletechklst.html'
    model = CheckList
    success_message = 'DeletechklstOK'
    success_url = reverse_lazy('app_home:main')


class ChklstDisplayView(BSModalReadView):
    context = {'title': 'Chklistdisplay'}
    template_name = 'app_create_chklst/dialogboxes/displaychklst.html'

    def get(self, request, **kwargs):
        pk = kwargs['pk']
        checklist = CheckList.objects.get(pk=pk)
        details = checklist.chklst_detail()
        self.context['details'] = details
        self.context['checklist'] = checklist
        return render(request, self.template_name, context=self.context)


@csrf_exempt
@transaction.atomic
def create_chklst(request):
    """
    Create checklist --> Ajax request
    :param request: all the checklist + lines & categories
    :return: OK or Erreur (just OK is verified !)
    """
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        print(request_data)
        chk_key = request_data['chk_key']
        chk_title = request_data['chk_title']
        chk_enable = request_data['chk_enable']
        if 'chk_company' in request_data:
            chk_company = Company.objects.get(pk=request_data['chk_company'])
        else:
            chk_company = request.user.user_company

        lines = request_data['lines']
        position = 0
        new_checklist, created = CheckList.objects.update_or_create(chk_key=chk_key,
                                                                    chk_title=chk_title,
                                                                    chk_enable=chk_enable,
                                                                    chk_company=chk_company,
                                                                    chk_user_id=request.user.id)
        new_checklist.save()
        CheckListLine.objects.filter(chk_line_checklist=new_checklist).delete()
        CheckListCategory.objects.filter(chk_cat_checklist=new_checklist).delete()
        for line in lines:
            print(line)
            cat_line = line[0:3]
            catline_id = line[4:]
            print(catline_id)
            if cat_line == "cat":
                category = Category.objects.get(pk=int(catline_id))
                chkcat, created = CheckListCategory.objects.update_or_create(chk_cat_position=position,
                                                                    chk_cat_category=category,
                                                                    chk_cat_checklist=new_checklist)
                chkcat.save()
            else:
                line = Line.objects.get(pk=int(catline_id))
                chkline, created = CheckListLine.objects.update_or_create(chk_line_position=position,
                                                                 chk_line_line=line,
                                                                 chk_line_checklist=new_checklist)
                chkline.save()
            position += 1
    data = {'data': 'OK'}
    return JsonResponse(data)


class ChkLstCreateView(View):
    context = {'title': 'Chklstcreate'}
    form = CheckListCreateForm
    success_url = reverse_lazy('app_home:main')

    def get(self, request):
        if request.user.is_superuser:
            categories = Category.objects.all().order_by('cat_company')
            lines = Line.objects.all().order_by('line_company')
        else:
            categories = Category.objects.filter(Q(cat_company=request.user.user_company) & Q(cat_enable=True))\
                .order_by('cat_key')
            lines = Line.objects.filter(Q(line_company=request.user.user_company) & Q(line_enable=True))\
                .order_by('line_key')
        self.context['categories'] = categories
        self.context['lines'] = lines
        self.context['form'] = self.form
        return render(request, 'app_create_chklst/createchklst.html', context=self.context)

    def post(self, request):
        return self.success_url


# noinspection PyTypeChecker
class ChkLstUpdateView(View):
    context = {'title': 'Chklstupdate'}
    form = CheckListCreateForm
    success_url = reverse_lazy('app_home:main')

    def get(self, request, pk):
        if request.user.is_superuser:
            categories = Category.objects.all().order_by('cat_company')
            lines = Line.objects.all().order_by('line_company')
        else:
            categories = Category.objects.filter(Q(cat_company=request.user.user_company) & Q(cat_enable=True))\
                .order_by('cat_key')
            lines = Line.objects.filter(Q(line_company=request.user.user_company) & Q(line_enable=True))\
                .order_by('line_key')
        self.context['categories'] = categories
        self.context['lines'] = lines
        checklist = CheckList.objects.get(pk=pk)
        details = checklist.chklst_detail()
        self.context['details'] = details
        self.context['checklist'] = checklist
        self.context['form'] = self.form(initial={'chk_key': checklist.chk_key,
                                                  'chk_title': checklist.chk_title,
                                                  'chk_enable': checklist.chk_enable,
                                                  'chk_company': checklist.chk_company, })
        return render(request, 'app_create_chklst/updatechklst.html', context=self.context)

    def post(self, request):
        return self.success_url

"""
list=[]
chk=CheckList.objects.get(id=3)  // 1 checklist
lines=chk.chk_line.all()    // toutes les lignes de la checklist
// line=lines[0]   // la premiere
// line.cll_lines.all() --> toutes les checklistelines ou apparait la ligne
// line.cll_lines.filter(chk_line_checklist_id=chk.id) --> LA ligne/position de la ligne...
list=[]
chk=CheckList.objects.get(id=3)
lines=chk.chk_line.all()
for line in lines:
    un=line.cll_lines.get(chk_line_checklist_id=chk.id).chk_line_position
    deux=line.line_wording
    trois=line.id
    tup=(un,deux,trois,'line')
    list.append(tup)


categories=chk.chk_category.all()
for category in categories:
    un=category.clc_categories.get(chk_cat_checklist_id=chk.id).chk_cat_position
    deux=category.cat_wording
    trois=category.id
    tup=(un,deux,trois,'cat')
    list.append(tup)

    
list2=sorted(list, key=lambda tup: tup[0])





# ...     myline=line.cll_lines.filter(chk_line_checklist_id=chk.id)
# ...     for maligne in myline:
# ...             un=maligne.chk_line_position
#                 deux=line.line_wording
                tup=(un,deux)
                list.append[(tup)]
faire la même avec les categories
list2=sorted(list, key=lambda tup: tup[0]) --> tri de la liste sur position

1
5

"""