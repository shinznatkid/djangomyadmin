from __future__ import unicode_literals
from django.db import connections
from django.conf import settings
from django.db import OperationalError
from .models import *
import time


class InvalidUsernameorpassword(Exception):
    pass


class Database(object):

    def __init__(self, username, password, database_name=''):
        self.username      = username
        self.password      = password
        self.database_name = database_name
        if 'session' not in settings.DATABASES:
            settings.DATABASES['session'] = {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '',
                'HOST': '127.0.0.1',
                'PORT': '3306',
            }
        settings.DATABASES['session'].update({
            'USER': username,
            'PASSWORD': password,
        })
        self.connection = connections['session']
        try:
            with self.connection.cursor() as cursor:
                if database_name:
                    cursor.execute('USE %s' % database_name)
        except OperationalError:
            raise InvalidUsernameorpassword()
        settings.DATABASES['schema'] = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'information_schema',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'USER': username,
            'PASSWORD': password,
        }
        self.connection_schema = connections['schema']
        self.query_time = None

    def show_databases(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SHOW DATABASES')
            return [x[0] for x in cursor.fetchall()]

    def show_tables(self, database_name=None, simple=False):
        if not database_name:
            database_name = self.database_name
        if simple:
            with self.connection.cursor() as cursor:
                cursor.execute('SHOW TABLES')
                return [x[0] for x in cursor.fetchall()]
        else:
            return list(Tables.objects.using('schema').filter(table_schema=database_name).all())

    def get_columns(self, table_name):
        return list(Columns.objects.using('schema').filter(table_schema=self.database_name, table_name=table_name).all())

    def query(self, q):
        t1 = time.clock()
        with self.connection.cursor() as cursor:
            cursor.execute(q)
            records = cursor.fetchall()
            t2 = time.clock()
            self.query_time = t2 - t1
            return records

    def display_query(self, q):
        t1 = time.clock()
        with self.connection.cursor() as cursor:
            cursor.execute(q)
            records = cursor.fetchall()
            t2 = time.clock()
            self.query_time = t2 - t1
            new_records = []
            for record in records:
                new_record = []
                for x in record:
                    str_x = unicode(x)
                    str_x = str_x if len(str_x) < 51 else str_x[:50] + '...'
                    new_record.append(str_x)
                new_records.append(new_record)
            return new_records

    def create_databases(self, database_name, collation=None):
        if not collation:
            collation = 'utf8_general_ci'

        if database_name not in self.show_databases():
            with self.connection.cursor() as cursor:
                command = 'CREATE DATABASE IF NOT EXISTS {} COLLATE {}'.format(database_name, collation)
                cursor.execute(command)
