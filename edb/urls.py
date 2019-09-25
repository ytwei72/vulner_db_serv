from django.urls import path
from . import views

urlpatterns = [
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 漏洞信息

    # 漏洞信息的查询、读取、添加、修改、删除
    path('query', views.query, name='edb_query'),
    path('fetch', views.fetch, name='edb_fetch'),
    path('search', views.search, name='edb_search'),
    path('add', views.add, name='edb_add'),
    path('update', views.update, name='edb_update'),
    path('delete', views.delete, name='edb_delete'),
    path('query-type', views.query_type, name='edb_query_type'),
    path('query-platform', views.query_platform, name='edb_query_platform'),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 漏洞POC

    # 漏洞poc的查询、读取
    path('poc/query', views.poc_query, name='edb_poc_query'),
    path('poc/fetch', views.poc_fetch, name='edb_poc_fetch'),
    path('poc/add', views.poc_add, name='edb_poc_add'),
    path('poc/update', views.poc_update, name='edb_poc_update'),
    path('poc/delete', views.poc_delete, name='edb_poc_delete'),
    path('poc/search', views.poc_search, name='edb_poc_search'),
]
