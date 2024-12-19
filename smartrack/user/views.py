from django.shortcuts import render, redirect
from django.conf import settings
import pyrebase
import json

# Initialize Firebase
firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
auth = firebase.auth()

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Sign in user with Firebase
            user = auth.sign_in_with_email_and_password(email, password)
            
            # Store user info in session
            session_data = {
                'uid': user['localId'],
                'idToken': user['idToken'],
                'email': user['email']
            }
            request.session['user'] = session_data
            
            print("Login successful for:", email)  # Debug print
            return redirect('dashboard:home')
            
        except Exception as e:
            print("Firebase Auth Error:", str(e))  # Debug print
            message = "Authentication failed. Please check your credentials."
            return render(request, 'login.html', {'message': message})
    
    return render(request, 'login.html')

def logout_view(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('user:login')