from django.shortcuts import render, redirect
from .forms import LoginForm
from django.conf import settings
from .database import Database, InvalidUsernameorpassword
from .models import *


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


@dblogin_required
def index(request):
    username = request.session.get('username')
    password = request.session.get('password')
    # if not username:
    #     return redirect('djangomyadmin.login')
    db = Database(username, password)
    data = {
        'databases': db.show_databases(),
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
    username = request.session.get('username')
    password = request.session.get('password')
    db = Database(username, password, database_name)
    data = {
        'database_name': database_name,
        'tables': db.show_tables(),
    }
    return render(request, 'page/tables.html', data)


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
