from django.shortcuts import render, redirect
from django.conf import settings
import pyrebase
import json
import uuid

# Initialize Firebase
firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
auth = firebase.auth()

from django.shortcuts import render, redirect
from django.conf import settings
import pyrebase
import os
import cv2
import uuid

def register_view(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('name')
            images = request.FILES.getlist('face_images')
            
            # Firebase Authentication
            firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
            auth = firebase.auth()
            user = auth.create_user_with_email_and_password(email, password)
            
            # Create directory for user's images
            user_dir = os.path.join(settings.FACE_RECOGNITION_SETTINGS['TRAINING_PATH'], name)
            os.makedirs(user_dir, exist_ok=True)
            
            # Save face images
            for image in images:
                img_path = os.path.join(user_dir, f"{uuid.uuid4()}.jpg")
                with open(img_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                
                # Verify face in image
                img = cv2.imread(img_path)
                if img is None:
                    os.remove(img_path)
                    continue
                    
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                if len(faces) != 1:
                    os.remove(img_path)
                    continue
            
            return redirect('user:login')
            
        except Exception as e:
            print("Registration Error:", str(e))
            message = "Registration failed. Please try again."
            return render(request, 'register.html', {'message': message})
    
    return render(request, 'register.html')

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