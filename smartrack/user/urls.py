# user/urls.py
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
]