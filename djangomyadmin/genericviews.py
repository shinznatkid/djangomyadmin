# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.conf import settings


from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator


def dblogin_required(view_func):
    def decorator(request, *args, **kwargs):
        username = request.session.get('username')
        if not username:
            if 'djangomyadmin' in settings.DATABASES:
                username = settings.DATABASES['djangomyadmin']['USER']
                request.session['username'] = settings.DATABASES['djangomyadmin']['USER']
                request.session['password'] = settings.DATABASES['djangomyadmin']['PASSWORD']
        if username:
            return view_func(request, *args, **kwargs)
        return redirect('djangomyadmin.login')
    return decorator


class AjaxTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(AjaxTemplateView, self).get_context_data(**kwargs)
        context['template_ajax_name'] = self.template_ajax_name
        return context

    @method_decorator(dblogin_required)
    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            self.template_name = self.template_ajax_name
        return super(AjaxTemplateView, self).dispatch(*args, **kwargs)
