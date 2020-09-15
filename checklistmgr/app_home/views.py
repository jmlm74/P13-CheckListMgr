from django.shortcuts import render

# Create your views here.
from django.views import View


class Index(View):
    def get(self, request):
        return render(request, 'app_home/home.html', {})
