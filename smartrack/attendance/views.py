from django.shortcuts import render

# Create your views here.
import cv2
import numpy as np
import face_recognition
import os
import pickle
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.http import StreamingHttpResponse
from .models import Attendance

class FaceDetector:
    def __init__(self):
        self.path = 'Training_images'
        self.encodings_file = 'encodings.pkl'
        self.known_face_encodings = []
        self.known_names = []
        self.load_encodings()
    
    def load_encodings(self):
        if os.path.exists(self.encodings_file):
            with open(self.encodings_file, 'rb') as f:
                self.known_face_encodings, self.known_names = pickle.load(f)
        else:
            self.generate_encodings()
    
    def generate_encodings(self):
        images = []
        names = []
        for person_name in os.listdir(self.path):
            person_path = os.path.join(self.path, person_name)
            if os.path.isdir(person_path):
                for img_name in os.listdir(person_path):
                    img_path = os.path.join(person_path, img_name)
                    img = cv2.imread(img_path)
                    if img is not None:
                        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        face_encoding = face_recognition.face_encodings(rgb_img)
                        if face_encoding:
                            self.known_face_encodings.append(face_encoding[0])
                            self.known_names.append(person_name)
        
        with open(self.encodings_file, 'wb') as f:
            pickle.dump((self.known_face_encodings, self.known_names), f)

def gen_frames(camera):
    face_detector = FaceDetector()
    
    while True:
        success, frame = camera.read()
        if not success:
            break
            
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(face_detector.known_face_encodings, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                name = face_detector.known_names[first_match_index]
                
                # Mark attendance
                try:
                    Attendance.objects.create(name=name)
                except:
                    pass # Already marked for today
                
                # Draw box
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def mark_attendance(request):
    return render(request, 'attendance/mark_attendance.html')

def video_feed(request):
    return StreamingHttpResponse(gen_frames(cv2.VideoCapture(0)),
                               content_type='multipart/x-mixed-replace; boundary=frame')