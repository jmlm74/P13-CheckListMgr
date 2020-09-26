from io import StringIO, BytesIO
from PIL import Image
from django import forms

from app_user.models import User, UserLanguages, Company



class UserCheckListMgrFormLogin(forms.Form):
    username = forms.CharField(label="User")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    bot_catcher = forms.CharField(required=False,
                                  widget=forms.HiddenInput)

    class Meta:
        model = User
        # fields = ('username', 'password')


class UserCheckListMgrRegister(forms.Form):
    """
    Form creation user

    clean-picture valid the picture size (not resizing)
    """
    username = forms.CharField(label="Username", max_length=30)
    first_name = forms.CharField(label="first_name", max_length=30)
    last_name = forms.CharField(label="last_name", max_length=30)
    email = forms.EmailField(label="Email", max_length=200)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), max_length=50, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=50, label="Confirm", min_length=8)
    preferred_language = forms.ModelChoiceField(label="language", queryset=UserLanguages.objects.all(), initial=0)
    phone = forms.CharField(max_length=31, label="Phone")
    picture = forms.ImageField()
    company = forms.ModelChoiceField(label="Company", queryset=Company.objects.all().order_by('name'), initial="-------")
    admin = forms.BooleanField(initial=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password',
                  'confirm_password', 'phone', 'picture', 'company', ]

    def __init__(self, *args, **kwargs):
        super(UserCheckListMgrRegister, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['picture'].required = False
        self.fields['company'].required = False
        self.fields['company'].empty_label = "-------"
        self.fields['admin'].required = False
        self.fields['password'].widget.attrs = {'placeholder': '8 chars min'}
        self.fields['confirm_password'].widget.attrs = {'placeholder': '8 chars min'}

    def clean_picture(self):
        # picture is not in data --> no picture selected
        if not self.cleaned_data['picture']:
            self.cleaned_data['picture'] = ''
            return ''
        photo = self.cleaned_data['picture']
        if photo:
            photo_data = BytesIO(photo.read())
            image = Image.open(photo_data)
            width, height = image.size
            if width > 50 or height > 50:
                raise forms.ValidationError("Big_image")
            return photo
        else:
            return ''


class UserCheckListMgrList(forms.Form):
    pass
