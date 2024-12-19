from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('manage-employee/', views.manage_employee, name='manage_employee'),
]