from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from app_user.forms import UserCheckListMgrFormLogin

# Create your views here.
from django.views import View
from django.views.generic.base import TemplateView


class Index(View):
    context = {'title': "app_user-home-title"}
    template_name = 'app_home/home.html'
    form = UserCheckListMgrFormLogin

    def get(self, request):
        try:
            request.session['language']
        except KeyError:
            request.session['language'] = 'UK'
        self.context['form'] = self.form
        return render(request, self.template_name, context=self.context)

    def post(self, request):
        if self.form.is_valid():
            username = request.POST.get('username', False)
            password = request.POS.get('password', False)
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    print(f"Connection of {username}")  # for the logs
                    return HttpResponseRedirect(reverse('app_home:index'))  # return to the index
                else:
                    self.form.add_error(None, "Compte désactivé : Connexion refusée")
        self.context['form'] = self.form
        return render(request, self.template_name, context=self.context)


class LegalView(TemplateView):
    template_name = "app_home/legal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Legal'
        return context


class ContactView(TemplateView):
    template_name = "app_home/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact'
        return context

