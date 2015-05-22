# -*- coding: utf-8 -*-

import pkgutil
import json
import math
import sys

from django.core.urlresolvers import resolve, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from .models import Tables
from .forms import LoginForm
from .database import Database, InvalidUsernameorpassword
from .genericviews import AjaxTemplateView


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


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator


@dblogin_required
def index(request):
    username = request.session.get('username')
    password = request.session.get('password')

    # if not username:
    #     return redirect('djangomyadmin.login')

    database_name = None

    db = Database(username, password)
    if request.POST:
        if 'createDatabase' in request.POST:
            database_name = request.POST.get('database_name')
            collation = request.POST.get('collation')

            if database_name:
                db = Database(username, password)
                db.create_databases(database_name, collation)

    data = {
        'databases': db.show_databases(),
        'database_name': database_name,
    }
    return render(request, 'index.html', data)


def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username, password = form.save()
        request.session['username'] = username
        request.session['password'] = password
        try:
            Database(username, password)
            return redirect('djangomyadmin.index')
        except InvalidUsernameorpassword:
            pass  # show invalid user or pass
    data = {
        'form': form,
    }
    return render(request, 'login.html', data)


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    if 'password' in request.session:
        del request.session['password']
    return redirect('djangomyadmin.login')


class PageDatabaseView(AjaxTemplateView):

    template_name         = 'index.html'
    template_ajax_name    = 'page/databases.html'

    def dispatch(self, *args, **kwargs):
        username = self.request.session.get('username')
        password = self.request.session.get('password')
        self.db = Database(username, password)
        return super(PageDatabaseView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            self.get_context_data(
                databases=self.db.show_databases(),
            )
        )


@dblogin_required
def page_tables(request, database_name):
    print 'page_tables'
    username = request.session.get('username')
    password = request.session.get('password')
    db = Database(username, password, database_name)
    data = {
        'database_name': database_name,
        'tables': db.show_tables(),
    }
    return render(request, 'page/tables.html', data)


@dblogin_required
def page_create_table(request, database_name):
    print 'page_create_tables'
    username = request.session.get('username')
    password = request.session.get('password')
    db = Database(username, password, database_name)

    table_name = request.GET.get('table_name')
    columns_num = request.GET.get('columns_num')

    data = {
        'database_name': database_name,
        'table_name': table_name,
        'columns_num': columns_num,
    }
    return render(request, 'page/create_table.html', data)


@dblogin_required
@json_response
def ajax_create_table(request, database_name):

    username = request.session.get('username')
    password = request.session.get('password')

    columns_num = int(request.POST.get('columns_num'))
    table_name = request.POST.get('table_name')
    table_comments = request.POST.get('tbl_comments')
    table_storage = request.POST.get('tbl_storage_engine')
    table_collation = request.POST.get('tbl_collation')

    columns = list()
    for i in range(columns_num):
        name = request.POST.get('field_name[' + str(i) + ']')
        if name:
            column = dict(
                name=name,
                type=request.POST.get('field_type[' + str(i) + ']'),
                length=request.POST.get('field_length[' + str(i) + ']'),
                default_type=request.POST.get('field_default_type[' + str(i) + ']'),
                default_value=request.POST.get('field_default_value[' + str(i) + ']'),
                collation=request.POST.get('field_collation[' + str(i) + ']'),
                attribute=request.POST.get('field_attribute[' + str(i) + ']'),
                null=request.POST.get('field_null[' + str(i) + ']'),
                key=request.POST.get('field_key[' + str(i) + ']'),
                extra=request.POST.get('field_extra[' + str(i) + ']'),
                comments=request.POST.get('field_comments[' + str(i) + ']'),
            )
            columns.append(column)
    table_info = dict(
        name=table_name,
        comments=table_comments,
        storage=table_storage,
        collation=table_collation,
        columns=columns,
    )

    db = Database(username, password, database_name)
    return db.create_table(table_info)


@dblogin_required
def page_table(request, database_name, table_name):
    current_url_resolve = resolve(request.path_info)
    current_url_name = current_url_resolve.url_name
    current_url = reverse(current_url_name, args=current_url_resolve.args, kwargs=current_url_resolve.kwargs)

    pos = int(request.GET.get('pos', 0))
    if pos < 0:
        pos = 0
    max_rows = int(request.GET.get('max_rows', 30))
    if max_rows < 1:
        max_rows = 30

    username         = request.session.get('username')
    password         = request.session.get('password')
    db               = Database(username, password, database_name)
    columns          = db.get_columns(table_name)
    query            = 'SELECT * FROM `%s` LIMIT %s , %s' % (table_name, pos, max_rows)
    records          = db.display_query(query)
    query_time_usage = db.query_time
    table_engine     = Tables.objects.using('schema').filter(table_schema=database_name, table_name=table_name).first().engine
    count            = db.query('EXPLAIN SELECT * FROM `%s`' % (table_name))[0][8]
    count_str        = str(count)
    if table_engine == 'InnoDB':
        if count < 10000:
            count = db.query('SELECT COUNT(*) FROM `%s`' % (table_name))[0][0]
            count_str = str(count)
        else:
            count_str = '~%d' % count

    ''' Pagination '''
    nav_current_page = int(math.floor(pos / max_rows)) + 1
    latest_page      = int(math.floor(count / max_rows)) + 1
    nav_prev_page     = None
    nav_next_page     = None
    nav_first_page    = None
    nav_last_page     = None
    if nav_current_page > 1:
        nav_prev_page = (nav_current_page - 2) * max_rows if nav_current_page > 2 else 0
    if nav_current_page < latest_page:
        nav_next_page = nav_current_page * max_rows
    if nav_current_page > 2:
        nav_first_page = 0
    if nav_current_page < latest_page:
        nav_last_page = (latest_page - 1) * max_rows if latest_page > 0 else 0

    data = {
        'columns': columns,
        'records': records,
        'count': count_str,
        'query': query,
        'query_time_usage': '%.4f' % query_time_usage,
        'database_name': database_name,
        'table_name': table_name,
        'pos': pos,
        'pos_end': pos + len(records),

        'nav_current_page': nav_current_page,
        'nav_prev_page': nav_prev_page,
        'nav_next_page': nav_next_page,
        'nav_first_page': nav_first_page,
        'nav_last_page': nav_last_page,
        'current_url': current_url,
    }
    return render(request, 'page/sql.html', data)


@dblogin_required
def page_table_structure(request, database_name, table_name):
    username = request.session.get('username')
    password = request.session.get('password')
    db = Database(username, password, database_name)
    columns = db.get_columns(table_name)
    data = {
        'columns': columns,
        'database_name': database_name,
        'table_name': table_name,
    }
    return render(request, 'page/table_structure.html', data)


@dblogin_required
def sidebar_tables(request, database_name):
    username = request.session.get('username')
    password = request.session.get('password')
    db = Database(username, password, database_name)
    data = {
        'database_name': database_name,
        'tables': db.show_tables(simple=True),
    }
    return render(request, 'sidebar/tables.html', data)


class PageScriptsView(AjaxTemplateView):

    template_name         = 'index.html'
    template_ajax_name    = 'page/scripts.html'
    template_success_name = 'page/success.html'
    load_dir              = 'djangomyadminscripts'

    def load_all_modules_from_dir(self, dirname):
        from django.conf import settings
        import os.path
        full_dirname = os.path.join(settings.BASE_DIR, dirname)
        modules = []
        for importer, package_name, _ in pkgutil.iter_modules([full_dirname]):
            full_package_name = '%s.%s' % (dirname, package_name)
            if full_package_name not in sys.modules:
                __import__(full_package_name)
            module = sys.modules[full_package_name]
            for key in dir(module):
                if package_name.lower() == key.lower():
                    modules.append(getattr(module, key))
                    break
        return modules

    def dispatch(self, *args, **kwargs):
        self.modules = self.load_all_modules_from_dir(self.load_dir)
        username = self.request.session.get('username')
        password = self.request.session.get('password')
        self.db = Database(username, password)
        return super(PageScriptsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        modules = [module() for module in self.modules]
        return self.render_to_response(
            self.get_context_data(
                modules=modules,
            )
        )

    def post(self, request, *args, **kwargs):
        module_name = self.request.POST.get('module_name', None)
        modules = []
        check_module = None
        for module in self.modules:
            if module_name == module.name:
                data_module = module(self.request.POST)
                check_module = data_module
            else:
                data_module = module()
            modules.append(data_module)

        if check_module:
            if check_module.entity.is_valid():
                success = check_module.entity.execute(self.db)
                if not success:
                    return redirect('/')
                self.template_ajax_name = self.template_success_name
                return self.render_to_response(
                    self.get_context_data(success=success,))
        return self.render_to_response(
            self.get_context_data(modules=modules,))
