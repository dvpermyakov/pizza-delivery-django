# coding: utf-8

from django.contrib.auth.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from ....models import Company
from pizza_delivery_app.permissions.groups import CHIEF_GROUP, MENU_READ_PERMISSIONS, MENU_CHANGE_PERMISSIONS,\
    VENUE_CRUD_PERMISSIONS
from pizza_delivery_app.permissions.methods import add_group, add_permissions
from pizza_delivery_app.forms import SignUpForm
from django import forms


class CompanySignUpForm(SignUpForm):
    company_name = forms.CharField(label=u'Название компании', max_length=40)
    image = forms.ImageField(label=u'Картинка', widget=forms.ClearableFileInput())


def signup(request):
    def general_render(form):
        values = {
            'form': form,
            'title': 'Регистрация новой компании'
        }
        values.update(csrf(request))
        return render(request, 'web/signup.html', values)

    if request.method == 'GET':
        return general_render(CompanySignUpForm())
    elif request.method == 'POST':
        form = CompanySignUpForm(request.POST, request.FILES)
        if form.is_valid():
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            company_name = form.cleaned_data['company_name']
            chief = User.objects.create_user(login, email, password)
            add_group(chief, CHIEF_GROUP)
            add_permissions(chief, [MENU_READ_PERMISSIONS, MENU_CHANGE_PERMISSIONS, VENUE_CRUD_PERMISSIONS])
            Company.create(company_name, chief, form.cleaned_data['image'])
            chief = auth.authenticate(username=login, password=password)
            if chief and chief.is_active:
                auth.login(request, chief)
            return redirect('/web/main')
        else:
            return general_render(form)