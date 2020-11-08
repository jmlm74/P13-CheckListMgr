from datetime import datetime

from django import forms

from app_input_chklst.models import Material, Manager


class ChekListInput1Form(forms.Form):
    mat_designation = forms.ModelChoiceField(label="Material", queryset=Material.objects.all())
    mat_registration = forms.CharField(initial='', max_length=30, label="Serial/N", )
    mat_type = forms.CharField(initial='', max_length=30, label="Type")
    mat_model = forms.CharField(initial='', max_length=30, label="Model")
    mat_material = forms.CharField(initial='', max_length=30, label="material", )
    mat_manager = forms.CharField(initial='', max_length=30, label="manager", )
    mat_id = forms.IntegerField(initial=0)

    class Meta:
        fields = ['mat_designation', 'mat_registration', 'mat_type', 'mat_model', 'mat_material', 'mat_manager', ]

    def __init__(self, *args, **kwargs):
        super(ChekListInput1Form, self).__init__(*args, **kwargs)
        self.fields['mat_designation'].widget.attrs = {'size': '5', 'max_length': '5'}
        self.fields['mat_designation'].required = False
        self.fields['mat_registration'].required = False
        self.fields['mat_type'].required = False
        self.fields['mat_model'].required = False
        self.fields['mat_material'].required = False
        self.fields['mat_material'].widget.attrs['readonly'] = True
        self.fields['mat_manager'].required = False
        self.fields['mat_id'].required = False
        self.fields['mat_id'].initial = 0


class ChekListInput2Form(forms.Form):
    mgr_name = forms.ModelChoiceField(label="Owner", queryset=Manager.objects.all())
    mgr_contact = forms.CharField(initial='', max_length=30, label="Contact")
    mgr_phone = forms.CharField(initial='', max_length=31, label="Phone")
    mgr_email1 = forms.EmailField(initial='', max_length=255, label='Email1')
    mgr_email2 = forms.EmailField(initial='', max_length=255, label='Email2')
    mgr_id = forms.IntegerField(initial=0, label='id')

    class Meta:
        fields = ['mgr_name', 'mgr_contact', 'mgr_phone', 'mgr_email1', 'mgr_email2', 'mgr_id', ]

    def __init__(self, *args, **kwargs):
        super(ChekListInput2Form, self).__init__(*args, **kwargs)
        self.fields['mgr_name'].required = False
        self.fields['mgr_contact'].required = False
        self.fields['mgr_phone'].required = False
        self.fields['mgr_email1'].required = False
        self.fields['mgr_email2'].required = False
        self.fields['mgr_id'].required = False


class ChekListInput3Form(forms.Form):
    chk_title = forms.CharField(max_length=80,
                                label='Check-List title',
                                widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    chk_save = forms.CharField(max_length=1500, label='chk_save', widget=forms.Textarea)
    chk_remsave = forms.CharField(max_length=15000, label='remark_save')

    class Meta:
        fields = ['chk_title', 'chk_save']

    def __init__(self, *args, **kwargs):
        super(ChekListInput3Form, self).__init__(*args, **kwargs)
        self.fields['chk_title'].required = False
        self.fields['chk_save'].required = False
        self.fields['chk_remsave'].required = False


class ChekListInput4Form(forms.Form):
    cld_key = forms.CharField(max_length=15, label='Unique Key')
    cld_valid = forms.BooleanField(label='Checklist Valid')
    cld_remarks = forms.CharField(widget=forms.Textarea(attrs={'rows': '5', 'cols': '50', }))

    cld_fotosave = forms.CharField(max_length=1000, label='foto_save')

    class Meta:
        fields = ['cld_key', 'cld_valid', 'cld_remarks', 'cld_fotosave', ]

    def __init__(self, *args, **kwargs):
        super(ChekListInput4Form, self).__init__(*args, **kwargs)
        self.fields['cld_key'].required = False
        self.fields['cld_key'].initial = str(datetime.now().timestamp())[:15]
        self.fields['cld_valid'].required = False
        self.fields['cld_remarks'].required = False
        self.fields['cld_fotosave'].required = False
