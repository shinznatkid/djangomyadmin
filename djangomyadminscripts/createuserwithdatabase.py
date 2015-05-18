# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db import OperationalError, ProgrammingError
import cgi
import re


def addslashes(s):
    d = {
        '"': '\\"',
        "'": "\\'",
        "\0": "\\\0",
        "\\": "\\\\"
    }
    return ''.join(d.get(c, c) for c in s)


class CreateUserWithDatabaseForm(forms.Form):

    username      = forms.CharField(label=_("User name"), min_length=1)
    password      = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    cpassword     = forms.CharField(label=_("Confirm password"), widget=forms.PasswordInput())
    host          = forms.CharField(label=_("Host"), initial='localhost')
    database_name = forms.CharField(label=_("Database name"), help_text='Leave blank for same as username', required=False)  # Default = username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'[a-zA-Z0-9_-]+', username):
            raise forms.ValidationError(u'%s has not allowed letter.' % username)
        return username

    def clean(self):
        if (self.cleaned_data.get('password') != self.cleaned_data.get('cpassword')):
            raise ValidationError("Password do not match.")

        return self.cleaned_data

    def execute(self, db):
        username      = addslashes(self.cleaned_data.get('username'))
        host          = addslashes(self.cleaned_data.get('host'))
        password      = addslashes(self.cleaned_data.get('password'))
        database_name = addslashes(self.cleaned_data.get('database_name'))
        message       = ''
        if not database_name:
            database_name = username
        try:
            db.query("CREATE USER '%s'@'%s' IDENTIFIED BY '%s'" % (username, host, password))
        except OperationalError:
            message += 'Cannot create user (skipped).<br/>'
            pass  # Might be user exists
        try:
            db.query("CREATE DATABASE %s DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci" % (database_name))
        except ProgrammingError:
            message += 'Cannot create database (skipped).<br/>'
            pass  # Already exists
        db.query("GRANT ALL ON `%s`.* TO `%s`@%s" % (database_name, username, host))
        db.query("FLUSH PRIVILEGES")
        link_url = reverse('djangomyadmin.page_tables', kwargs=dict(database_name=database_name))
        success = '%sCreate user with database successful! go to <a href="%s">%s</a>' % (message, link_url, cgi.escape(database_name))
        return success


class CreateUserWithDatabase(object):

    name = 'CreateUserWithDatabase'
    verbose_name = 'Create user with database'
    form = CreateUserWithDatabaseForm

    def __str__(self):
        return self.verbose_name

    def __init__(self, *args, **kwargs):
        self.entity = self.form(*args, **kwargs)
