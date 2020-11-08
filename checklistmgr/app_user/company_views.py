from django.contrib import messages
from django.db.models import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import UpdateView

from sortable_listview import SortableListView

from app_user.forms import CompanyCreateForm, AddressCreateForm
from app_user.models import Company, Address


class ListCompaniesView(SortableListView):
    """
    List  companies --> ListView

    """
    context = {'title': "Companylist"}
    context_object_name = "companies"
    template_name = 'app_user/list_company.html'
    queryset = Company.objects.filter(~Q(address_id=1) & ~Q(address_id=None)).order_by('company_name')
    paginate_by = 5
    allowed_sort_fields = {"company_name": {'default_direction': '', 'verbose_name': 'Company'}, }
    default_sort_field = 'company_name'  # mandatory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Companylist"
        return context


class CreateCompanyView(View):
    """
    creat company view
    2 forms : The company (just the name --> model Company)
            : The address (may already exist !) --> model Address
    The creation is a 2 step creation : The company and then the address if it doesn't already exist
    """
    context = {'title': "Createcompany"}
    form = CompanyCreateForm
    form2 = AddressCreateForm
    template_name = 'app_user/create_company.html'

    def get(self, request):
        self.context['form'] = self.form(None)
        self.context['form2'] = self.form2(None)
        return render(request, self.template_name, context=self.context)

    def post(self, request):
        form = self.form(request.POST)  # the company
        form2 = self.form2(request.POST)  # the address
        if form.is_valid():
            if form2.is_valid():
                company = form.cleaned_data['company_name']
                memo = form2.cleaned_data['address_name']
                street_number = form2.cleaned_data['street_number']
                street_type = form2.cleaned_data['street_type']
                address1 = form2.cleaned_data['address1']
                address2 = form2.cleaned_data['address2']
                city = form2.cleaned_data['city']
                zipcode = form2.cleaned_data['zipcode']
                country = form2.cleaned_data['country']
                try:
                    # verify the address exists or not
                    new_memo = Address.objects.get(address_name__iexact=memo)
                except ObjectDoesNotExist:
                    # don't exist
                    new_memo = Address(address_name=memo,
                                       street_number=street_number,
                                       street_type=street_type,
                                       address1=address1,
                                       address2=address2,
                                       city=city,
                                       zipcode=zipcode,
                                       country=country)
                    new_memo.save()
                else:
                    # already exist --> modifications are applied
                    new_memo.street_number = street_number
                    new_memo.street_type = street_type
                    new_memo.address1 = address1
                    new_memo.address2 = address2
                    new_memo.city = city
                    new_memo.zipcode = zipcode
                    new_memo.country = country
                    new_memo.save()
                new_company = Company(company_name=company,
                                      address=new_memo)
                new_company.save()
                self.context['company_created'] = company
                messages.success(request, "RegisterOK")
        self.context['form'] = form
        self.context['form2'] = form2
        return render(request, self.template_name, self.context)


class EditCompanyView(UpdateView):
    """
    Modify Company --> same principle as the creation --> 2 steps
    """
    context = {'title': "Companyupdate"}
    form = CompanyCreateForm
    form2 = AddressCreateForm
    model = Company
    second_model = Address
    fields = ['company_name', 'address']
    template_name = 'app_user/create_company.html'
    # success_url = "/app_user/list_company/"

    def get_context_data(self, **kwargs):
        context = super(EditCompanyView, self).get_context_data(**kwargs)

        form_id = self.object.id
        company = Company.objects.get(pk=form_id)
        address = Address.objects.get(id=company.address_id)
        if 'form' not in context:
            context['form'] = self.form
        if 'form2' not in context:
            context['form2'] = self.form2(instance=address)
        context['id'] = form_id
        context['title'] = "Companyupdate"
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, pk):
        request.POST._mutable = True  # to modify the POST
        request.POST['update'] = True
        form = self.form(request.POST)
        form2 = self.form2(request.POST)
        # form is always in error --> duplicate name !!!
        if form2.is_valid():
            form._errors = {}
            company = request.POST['company_name']
            # company_address = form.cleaned_data['address']
            memo = form2.cleaned_data['address_name']
            street_number = form2.cleaned_data['street_number']
            street_type = form2.cleaned_data['street_type']
            address1 = form2.cleaned_data['address1']
            address2 = form2.cleaned_data['address2']
            city = form2.cleaned_data['city']
            zipcode = form2.cleaned_data['zipcode']
            country = form2.cleaned_data['country']
            try:
                new_memo = Address.objects.get(address_name__iexact=memo)
            except ObjectDoesNotExist:
                new_memo = Address(address_name=memo,
                                   street_number=street_number,
                                   street_type=street_type,
                                   address1=address1,
                                   address2=address2,
                                   city=city,
                                   zipcode=zipcode,
                                   country=country)
                new_memo.save()
            else:
                new_memo.street_number = street_number
                new_memo.street_type = street_type
                new_memo.address1 = address1
                new_memo.address2 = address2
                new_memo.city = city
                new_memo.zipcode = zipcode
                new_memo.country = country
                new_memo.save()
            upd_company = Company.objects.get(pk=pk)
            upd_company.address = new_memo
            upd_company.save()
            self.context['id'] = pk
            messages.success(request, "CompanyupdateOK")
            self.context['form'] = form
            self.context['form2'] = form2
            return render(request, self.template_name, self.context)

        else:
            self.context['form'] = form
            self.context['form2'] = form2
            return render(request, self.template_name, self.context)
