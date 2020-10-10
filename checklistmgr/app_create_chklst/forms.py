from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from app_create_chklst.models import Category, Line, CheckList
from app_user.models import Company


class CategoryModelForm(BSModalModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryModelForm, self).__init__(*args, **kwargs)
        self.fields['cat_company'].required = False

    def clean(self):
        super(CategoryModelForm, self).clean()
        try:
            if not self.cleaned_data['cat_company']:
                self.cleaned_data['cat_company'] = self.request.user.user_company
        except KeyError:
            self.cleaned_data['cat_company'] = self.request.user.user_company
        return self.cleaned_data


class LineModelForm(BSModalModelForm):
    class Meta:
        model = Line
        fields = '__all__'
        widgets = {'line_type': forms.RadioSelect, }

    def __init__(self, *args, **kwargs):
        super(LineModelForm, self).__init__(*args, **kwargs)
        self.fields['line_company'].required = False

    def clean(self):
        super(LineModelForm, self).clean()
        if not self.cleaned_data['line_company']:
            self.cleaned_data['line_company'] = self.request.user.user_company
        return self.cleaned_data


class CheckListCreateForm(forms.Form):
    chk_key = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size': '20'}))
    chk_title = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'size': '30'}))
    chk_enable = forms.BooleanField(initial=True)
    chk_company = forms.ModelChoiceField(queryset=Company.objects.all().order_by('company_name'),
                                         initial="-------")

    class Meta:
        model = CheckList
        Fields = ['chk_key', 'chk_title', 'chk_enable', 'chk_company', ]
