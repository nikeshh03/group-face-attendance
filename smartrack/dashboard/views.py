from django.shortcuts import render, redirect
from functools import wraps
from attendance.models import Attendance
from datetime import datetime, timedelta
from django.db.models import Q

def auth_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('user:login')
        return f(request, *args, **kwargs)
    return decorated_function

@auth_required
def home(request):
    context = {
        'user': request.session.get('user', {})
    }
    return render(request, 'dashboard.html', context)

@auth_required
def mark_attendance(request):
    return render(request, 'mark_attendance.html')

@auth_required
def view_attendance(request):
    attendance_records = Attendance.objects.all().order_by('-date', '-time')
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        attendance_records = attendance_records.filter(name__icontains=search_query)
    
    # Handle date filter
    date_filter = request.GET.get('date_filter', 'all')
    today = datetime.now().date()
    
    if date_filter == 'today':
        attendance_records = attendance_records.filter(date=today)
    elif date_filter == 'week':
        week_ago = today - timedelta(days=7)
        attendance_records = attendance_records.filter(date__gte=week_ago)
    elif date_filter == 'month':
        month_ago = today - timedelta(days=30)
        attendance_records = attendance_records.filter(date__gte=month_ago)
        
    context = {
        'attendance_records': attendance_records,
    }
    return render(request, 'view_attendance.html', context)