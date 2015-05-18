from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.index, name='djangomyadmin.index'),
    url(r'^login/$', views.login, name='djangomyadmin.login'),
    url(r'^logout/$', views.logout, name='djangomyadmin.logout'),

    url(r'^page/scripts/$', views.PageScriptsView.as_view(), name='djangomyadmin.page_scripts'),
    url(r'^page/databases$', views.page_databases, name='djangomyadmin.page_databases'),
    url(r'^page/database/(?P<database_name>[_a-zA-Z0-9]+)/tables/$', views.page_tables, name='djangomyadmin.page_tables'),
    url(r'^page/database/(?P<database_name>[_a-zA-Z0-9]+)/create_table/$', views.page_create_table, name='djangomyadmin.page_create_table'),
    url(r'^page/database/(?P<database_name>[_a-zA-Z0-9]+)/table/(?P<table_name>[_a-zA-Z0-9]+)/$', views.page_table, name='djangomyadmin.page_table'),
    url(r'^page/database/(?P<database_name>[_a-zA-Z0-9]+)/table/(?P<table_name>[_a-zA-Z0-9]+)/structure/$', views.page_table_structure, name='djangomyadmin.page_table_structure'),

    url(r'^sidebar/database/(?P<database_name>[_a-zA-Z0-9]+)/tables/$', views.sidebar_tables, name='djangomyadmin.sidebar_tables'),

    url(r'^ajax/(?P<database_name>[_a-zA-Z0-9]+)/create_table/$', views.ajax_create_table, name='djangomyadmin.ajax_create_table'),
)
