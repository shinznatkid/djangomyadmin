from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('djangomyadmin.views',
    url(r'^$', 'index', name='djangomyadmin.index'),
    url(r'^login/$', 'login', name='djangomyadmin.login'),
    url(r'^logout/$', 'logout', name='djangomyadmin.logout'),

    url(r'^page/databases$', 'page_databases', name='djangomyadmin.page_databases'),
    url(r'^page/database/(?P<database_name>[_a-zA-Z0-9]+)/tables/$', 'page_tables', name='djangomyadmin.page_tables'),
    url(r'^page/database/(?P<database_name>[_a-zA-Z0-9]+)/table/(?P<table_name>[_a-zA-Z0-9]+)/$', 'page_table', name='djangomyadmin.page_table'),
    url(r'^page/database/(?P<database_name>[_a-zA-Z0-9]+)/table/(?P<table_name>[_a-zA-Z0-9]+)/structure/$', 'page_table_structure', name='djangomyadmin.page_table_structure'),

    url(r'^sidebar/database/(?P<database_name>[_a-zA-Z0-9]+)/tables/$', 'sidebar_tables', name='djangomyadmin.sidebar_tables'),
)