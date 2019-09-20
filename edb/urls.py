from django.urls import path
from . import views

urlpatterns = [
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 漏洞信息

    # 漏洞信息的查询、读取、添加、修改、删除
    path('query', views.query, name='edb_query'),
    path('search', views.search, name='edb_search'),
    path('add', views.add, name='edb_add'),
    path('update', views.update, name='edb_update'),
    path('delete', views.delete, name='edb_delete'),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 漏洞利用方法

    # 漏洞利用方法的查询、读取
    path('methods/query', views.methods_query, name='edb_methods_query'),
    path('methods/fetch', views.methods_fetch, name='edb_methods_fetch'),
]
