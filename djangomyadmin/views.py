from django.shortcuts import render, redirect
from .forms import LoginForm
from django.conf import settings
from .database import Database, InvalidUsernameorpassword
from .models import *
from django.http import HttpResponse
import json


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


@dblogin_required
def page_databases(request):
    username = request.session.get('username')
    password = request.session.get('password')

    db = Database(username, password)
    data = {
        'databases': db.show_databases(),
    }
    return render(request, 'page/databases.html', data)


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
def page_table(request, database_name, table_name):
    pos = int(request.GET.get('pos', 0))
    username = request.session.get('username')
    password = request.session.get('password')
    db = Database(username, password, database_name)
    columns = db.get_columns(table_name)
    query = 'SELECT * FROM `%s` LIMIT %s , 30' % (table_name, pos)
    records = db.display_query(query)
    query_time_usage = db.query_time
    table_engine = Tables.objects.using('schema').filter(table_schema=database_name, table_name=table_name).first().engine
    count = db.query('EXPLAIN SELECT * FROM `%s`' % (table_name))[0][8]
    if table_engine == 'InnoDB':
        count = '~%d' % count
    data = {
        'columns': columns,
        'records': records,
        'count': count,
        'query': query,
        'query_time_usage': '%.4f' % query_time_usage,
        'database_name': database_name,
        'table_name': table_name,
        'pos': pos,
        'pos_end': pos + len(records),
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


def sidebar_tables(request, database_name):
    username = request.session.get('username')
    password = request.session.get('password')
    db = Database(username, password, database_name)
    data = {
        'database_name': database_name,
        'tables': db.show_tables(simple=True),
    }
    return render(request, 'sidebar/tables.html', data)


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
@json_response
def ajax_delete_table(request, database_name, table_name):

    username = request.session.get('username')
    password = request.session.get('password')

    db = Database(username, password, database_name)    
    return db.drop_table(table_name)