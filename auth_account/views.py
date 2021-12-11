from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .forms import LoginForm, CreateAccountForm


class Login(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm


class Logout(View):
    redirect_url_name = 'home'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse(self.redirect_url_name))


class CreateAccount(View):
    template_name = 'create_account.html'
    form = CreateAccountForm

    def get(self, request):
        self.form.base_fields['username'].widget.attrs.update({'class': 'form-control'})
        self.form.base_fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.form.base_fields['password2'].widget.attrs.update({'class': 'form-control'})
        return render(request, template_name=self.template_name, context={'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return HttpResponseRedirect(reverse('home'))
        else:
            self.form = form
            return self.get(request)

