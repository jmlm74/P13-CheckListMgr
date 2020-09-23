from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.views.generic.edit import CreateView
from app_user.models import User

from app_user.forms import UserCheckListMgrRegister

"""
class RegisterView(CreateView):
    model = User
    context = {'title': 'Register'}
    # fields = ['username', 'password', 'first_name', 'last_name', 'admin', 'preferred_language']
    template_name = 'app_user/register.html'
    form_class = UserCheckListMgrRegister

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['title'] = "Register"
        return context



"""
class RegisterView(View):
    context = {'title': "Register"}
    template_name = 'app_user/register.html'
    form = UserCheckListMgrRegister

    def get(self, request):
        try:
            request.session['language']
        except KeyError:
            request.session['language'] = 'UK'
        self.context['form'] = self.form(None)
        return render(request, self.template_name, context=self.context)

    def post(self, request):
        form = UserCheckListMgrRegister(request.POST, request.FILES)
        if form.is_valid():
            try:
                print(request.FILES['picture'])
            except MultiValueDictKeyError:
                pass
            if request.POST['password'] == request.POST['confirm_password']:
                try:
                    new_user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password'],
                        preferred_language=form.cleaned_data['preferred_lang'],
                        phone=form.cleaned_data['phone'],
                        picture=form.cleaned_data['picture']
                    )
                except IntegrityError:
                    form.add_error(None, 'Errdupleuser')
                else:
                    if new_user:
                        form = UserCheckListMgrRegister()
                    else:
                        form.add_error(None, 'Errcreateuser')
            else:
                form.add_error(None, 'Errpswconfir')
        self.context['form'] = form
        return render(request, self.template_name, self.context)

@login_required
def user_logout(request):
    logout(request)
    print("logout")
    return HttpResponseRedirect(reverse('app_home:index'))