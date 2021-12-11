from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import LoginForm


class Login(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm


class Logout(View):
    redirect_url_name = 'home'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse(self.redirect_url_name))
