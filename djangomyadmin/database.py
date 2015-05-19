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
        if database_name not in self.show_databases():
            with self.connection.cursor() as cursor:
                if not collation:
                    command = 'CREATE DATABASE {}'.format(database_name)
                else:
                    command = 'CREATE DATABASE {} COLLATE {}'.format(database_name, collation)
                cursor.execute(command)

    def create_table(self, table_info):
        if table_info['name'] not in self.show_tables():

            column_definitions = list()
            primary_key = list()
            unique_key = list()
            index_key = list()
            fulltext = list()

            for column in table_info['columns']:
                reference_definition = None
                column_def = '{} {} '.format(column['name'], column['type'])
                if column['length']:
                    column_def += '({}) '.format(column['length'])

                if column['attribute']:
                    if 'CURRENT_TIMESTAMP' in column['attribute']:
                        reference_definition = '{} '.format(column['attribute'])
                    else:
                        column_def += '{} '.format(column['attribute'])

                if any(s in column['type'] for s in ['CHAR', 'TEXT', 'SET', 'ENUM']) and column['collation']:
                        column_def += 'COLLATE {} '.format(column['collation'])

                if column['null']:
                    column_def += 'NULL '
                else:
                    column_def += 'NOT NULL '

                if column['default_type'] != 'NONE':
                    if column['default_type'] != 'USER_DEFINED':
                        column_def += 'DEFAULT {} '.format(column['default_type'])
                    else:
                        column_def += 'DEFAULT {} '.format(column['default_value'])

                if column['extra']:
                    column_def += 'AUTO_INCREMENT '

                if column['comments']:
                    column_def += 'COMMENT "{}" '.format(column['comments'])

                if reference_definition:
                    column_def += reference_definition

                column_definitions.append(column_def)

                if column['key'] == 'PRIMARY':
                    primary_key.append(column['name'])
                elif column['key'] == 'UNIQUE':
                    unique_key.append(column['name'])
                elif column['key'] == 'INDEX':
                    index_key.append(column['name'])
                elif column['key'] == 'FULLTEXT':
                    fulltext.append(column['name'])

            if primary_key:
                index_def = 'PRIMARY KEY ({})'.format(','.join(primary_key))
                column_definitions.append(index_def)
            if unique_key:
                index_def = 'UNIQUE ({})'.format(','.join(unique_key))
                column_definitions.append(index_def)
            if index_key:
                index_def = 'INDEX ({})'.format(','.join(index_key))
                column_definitions.append(index_def)
            if fulltext:
                index_def = 'FULLTEXT ({})'.format(','.join(fulltext))
                column_definitions.append(index_def)

            table_options = 'ENGINE={} '.format(table_info['storage'])

            if table_info['collation']:
                table_options += 'COLLATE={} '.format(table_info['collation'])

            if table_info['comments']:
                table_options += 'COMMENT="{}" '.format(table_info['comments'])

            command = 'CREATE TABLE {}({}){}'.format(table_info['name'], ','.join(column_definitions), table_options)
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(command)
                return dict(success=True)
            except Exception as ex:
                return dict(success=False, msg=str(ex))
        else:
            return dict(success=False, msg='This table exist.')
