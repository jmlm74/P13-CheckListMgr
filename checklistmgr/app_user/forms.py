from django import forms
from app_user.models import User


class UserCheckListMgrFormLogin(forms.ModelForm):
    username = forms.CharField(label="Utilisateur")
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    bot_catcher = forms.CharField(required=False,
                                  widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('username', 'password')





