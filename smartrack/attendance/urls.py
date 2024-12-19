from django.urls import path
from . import views

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('video_feed/', views.video_feed, name='video_feed'),
]