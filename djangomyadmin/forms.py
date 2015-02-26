# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, required=False)

    def save(self):
        return (self.cleaned_data['username'], self.cleaned_data['password'])
