# coding: utf-8

__author__ = 'dvpermyakov'

from django.shortcuts import render, redirect
from django.contrib import auth
from django import forms
from django.core.context_processors import csrf
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required


class LoginForm(forms.Form):
    login = forms.CharField(label=u'Логин', max_length=40)
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())

    def is_valid(self):
        valid = super(LoginForm, self).is_valid()
        if not valid:
            return valid
        user = auth.authenticate(username=self.cleaned_data['login'], password=self.cleaned_data['password'])
        if not user or not user.is_active:
            self._errors['login'] = ErrorList([u'Пароль или логин неверен'])
            return False
        return True


def login(request):
    def general_render(form):
        values = {
            'form': form
        }
        values.update(csrf(request))
        return render(request, 'web/login.html', values)

    if request.user.is_authenticated():
        return redirect('/web/main')

    if request.method == 'GET':
        return general_render(LoginForm())
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user and user.is_active:
                auth.login(request, user)
                return redirect('/web/main')
        else:
            return general_render(form)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/web/login')