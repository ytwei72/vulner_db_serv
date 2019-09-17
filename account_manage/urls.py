from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_account, name='register_account'),
    path('activate', views.activate_account, name='activate_account'),
    path('setrole', views.set_account_role, name='set_account_role'),
    path('verify-pwd', views.verify_password, name='verify_password'),
    path('unlock', views.unlock_account, name='unlock_account'),
]
