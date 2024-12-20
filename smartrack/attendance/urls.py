from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),  # Changed from mark_attendance_view
    path('video-feed/', views.video_feed, name='video_feed'),
]