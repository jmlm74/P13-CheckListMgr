from bootstrap_modal_forms.forms import BSModalModelForm
from django.core.exceptions import ValidationError

from app_input_chklst.models import Manager, Material
from app_user.models import Address


class ManagerCreateForm(BSModalModelForm):
    """
    create/update manager form
    Clean --> add the user company in the manager record (not visible for the user !)
    """
    class Meta:
        model = Manager
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ManagerCreateForm, self).__init__(*args, **kwargs)
        self.fields['mgr_contact'].required = False
        self.fields['mgr_phone'].required = False
        self.fields['mgr_email1'].required = False
        self.fields['mgr_email2'].required = False
        self.fields['mgr_address'].required = False
        self.fields['mgr_company'].required = False
        self.fields['mgr_address'].initial = '----------'
        self.fields['mgr_company'].initial = None

    def clean(self):
        super(ManagerCreateForm, self).clean()
        if self.request.user.admin and self.cleaned_data['mgr_company'] is None:
            self.cleaned_data['mgr_company'] = self.request.user.user_company
        return self.cleaned_data


class AddressCreateForm(BSModalModelForm):
    """
    Address create/update form
    """
    class Meta:
        model = Address
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddressCreateForm, self).__init__(*args, **kwargs)
        self.fields['street_number'].required = False
        self.fields['street_number'].widget.attrs = {'input type': 'number', 'size': '5', 'min': '0'}
        self.fields['street_type'].required = False
        self.fields['street_type'].widget.attrs = {'size': '10'}
        self.fields['address2'].required = False
        self.fields['address2'].widget.attrs = {'size': '60', 'max_length': '150'}
        self.fields['address1'].required = False
        self.fields['address1'].widget.attrs = {'size': '60', 'max_length': '150'}
        self.fields['zipcode'].widget.attrs = {'size': '10', 'max_length': '20'}
        self.fields['city'].widget.attrs = {'size': '30', 'max_length': '50'}
        self.fields['country'].widget.attrs = {'size': '30', 'max_length': '40'}
        self.fields['country'].initial = 'France'


class MaterialCreateForm(BSModalModelForm):
    """
    Material update/create form
    clean --> add the user company
              if secondary material add the primary material manager automatically
              validate a manager has benn set (by user or automatically)
    """

    class Meta:
        model = Material
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MaterialCreateForm, self).__init__(*args, **kwargs)
        self.fields['mat_designation'].widget.attrs = {'size': '20', 'max_length': '30'}
        self.fields['mat_registration'].required = False
        self.fields['mat_registration'].widget.attrs = {'size': '20', 'max_length': '30'}
        self.fields['mat_type'].required = False
        self.fields['mat_type'].widget.attrs = {'size': '20', 'max_length': '30'}
        self.fields['mat_model'].required = False
        self.fields['mat_model'].widget.attrs = {'size': '20', 'max_length': '30'}
        self.fields['mat_material'].required = False
        self.fields['mat_material'].initial = '-------'
        self.fields['mat_manager'].widget.attrs = {'style': 'width: 150px;'}
        self.fields['mat_material'].widget.attrs = {'style': 'width: 150px;'}
        self.fields['mat_manager'].required = False
        self.fields['mat_company'].required = False

    def clean(self):
        super(MaterialCreateForm, self).clean()
        # print(self.cleaned_data)
        if(self.cleaned_data['mat_company']) is None:
            self.cleaned_data['mat_company'] = self.request.user.user_company
        if self.cleaned_data['mat_material'] is not None:
            self.cleaned_data['mat_manager'] = self.cleaned_data['mat_material'].mat_manager
        if self.cleaned_data['mat_manager'] is None:
            raise ValidationError('CreatemgrKOmatexp')
        return self.cleaned_data
