from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('retrieve/', views.retrieve, name='retrieve'),
    path('fetch/', views.fetch, name='fetch'),
    path('level-stat/', views.level_stat, name='level-stat'),
    path('month-stat/', views.monthly_stat, name='month-stat'),
    path('yearly-stat/', views.yearly_stat, name='yearly-stat'),
    path('discoverer-stat/', views.discoverer_stat, name='discoverer-stat'),
    path('fix-stat/', views.fix_stat, name='fix-stat'),
    path('vul-type-stat/', views.vul_type_stat, name='vul-type-stat'),
]
