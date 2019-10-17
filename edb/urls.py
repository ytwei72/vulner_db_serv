from django.urls import path
from . import views

urlpatterns = [
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 漏洞信息

    # 漏洞信息的查询、读取、添加、修改、删除
    path('query', views.query, name='edb_query'),
    # 通过 id 精确查询
    path('fetch', views.fetch, name='edb_fetch'),
    # 查找特定漏洞（oracle / ssh / 西门子）
    path('filter', views.filter, name='edb_filter'),
    # 模糊查询
    path('search', views.search, name='edb_search'),
    path('add', views.add, name='edb_add'),
    path('update', views.update, name='edb_update'),
    path('delete', views.delete, name='edb_delete'),
    path('query-type', views.query_type, name='edb_query_type'),
    path('query-platform', views.query_platform, name='edb_query_platform'),
    path('exportxls', views.export_excel, name='edb_export_excel'),
    path('max-id', views.max_id, name='edb_max_id'),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 漏洞POC

    # 漏洞poc的查询、读取
    path('poc/query', views.poc_query, name='edb_poc_query'),
    # 通过 id 精确查询
    path('poc/fetch', views.poc_fetch, name='edb_poc_fetch'),
    path('poc/add', views.poc_add, name='edb_poc_add'),
    path('poc/update', views.poc_update, name='edb_poc_update'),
    path('poc/delete', views.poc_delete, name='edb_poc_delete'),
    # 模糊查询
    path('poc/search', views.poc_search, name='edb_poc_search'),
    path('poc/download', views.poc_download, name='edb_poc_download'),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 漏洞统计
    path('stat/verified', views.stat_verified, name='edb_stat_verified'),
    path('stat/years', views.stat_years, name='edb_stat_years'),
    path('stat/platform', views.stat_platform, name='edb_stat_platform'),
    path('stat/type', views.stat_type, name='edb_stat_type'),
]
