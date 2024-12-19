from django.shortcuts import render, redirect
from functools import wraps

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
def manage_employee(request):
    return render(request, 'manage_employee.html')