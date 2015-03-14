# coding: utf-8

from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    login = forms.CharField(label=u'Логин', max_length=40)
    email = forms.EmailField(label=u'Email', max_length=40)
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
    repeated_password = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput())

    def is_valid(self):

        valid = super(SignUpForm, self).is_valid()
        if not valid:
            return valid
        if self.cleaned_data['password'] != self.cleaned_data['repeated_password']:
            self._errors['repeated_password'] = ErrorList([u'Пароли не совпадают'])
            return False
        if User.objects.filter(username=self.cleaned_data['login']).count():
            self._errors['login'] = ErrorList([u'Этот логин уже занят'])
            return False
        return True