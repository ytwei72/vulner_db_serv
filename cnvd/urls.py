from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cnvd_index'),

    # 查询
    path('query-page/', views.query_page, name='cnvd_query_page'),
    path('query/', views.query, name='cnvd_query'),

    # 统计
    path('level-stat/', views.level_stat, name='cnvd_level_stat'),
    path('month-stat/', views.monthly_stat, name='cnvd_month_stat'),
    path('yearly-stat/', views.yearly_stat, name='cnvd_yearly_stat'),
    path('discoverer-stat/', views.discoverer_stat, name='cnvd_discoverer_stat'),
    path('fix-stat/', views.fix_stat, name='cnvd_fix_stat'),
    path('vul-type-stat/', views.vul_type_stat, name='cnvd_vul_type_stat'),
]
