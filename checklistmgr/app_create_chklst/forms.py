from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from app_create_chklst.models import Category, Line


class CategoryModelForm(BSModalModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryModelForm, self).__init__(*args, **kwargs)
        self.fields['cat_company'].required = False

    def clean(self):
        super(CategoryModelForm, self).clean()
        if not self.cleaned_data['cat_company']:
            self.cleaned_data['cat_company'] = self.request.user.user_company
        return self.cleaned_data


class LineModelForm(BSModalModelForm):
    class Meta:
        model = Line
        fields = '__all__'
        widgets = {'line_type': forms.RadioSelect, }
        labels = {'line_key': 'TOTO'}

    def __init__(self, *args, **kwargs):
        super(LineModelForm, self).__init__(*args, **kwargs)
        self.fields['line_company'].required = False
        self.fields['line_type'].label = "TOTO"


    def clean(self):
        super(LineModelForm, self).clean()
        if not self.cleaned_data['line_company']:
            self.cleaned_data['line_company'] = self.request.user.user_company
        return self.cleaned_data
