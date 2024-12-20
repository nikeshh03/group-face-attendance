import cv2
import numpy as np
import face_recognition
import os
import pickle
from datetime import datetime

path = 'Training_images'
images = []
classNames = []
encodeListKnown = []

# Load encodings from file if available
encodings_file = 'encodings.pkl'
if os.path.exists(encodings_file):
    with open(encodings_file, 'rb') as f:
        encodeListKnown, classNames = pickle.load(f)
    print('Encodings loaded from file')
else:
    # Loop through each person's directory
    for person_name in os.listdir(path):
        person_path = os.path.join(path, person_name)
        if os.path.isdir(person_path):
            for img_name in os.listdir(person_path):
                img_path = os.path.join(person_path, img_name)
                curImg = cv2.imread(img_path)
                if curImg is not None:
                    images.append(curImg)
                    classNames.append(person_name)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodes = face_recognition.face_encodings(img)
            if encodes:
                encodeList.append(encodes[0])
        return encodeList

    # Generate encodings for all images
    encodeListKnown = findEncodings(images)

    # Save encodings to file
    with open(encodings_file, 'wb') as f:
        pickle.dump((encodeListKnown, classNames), f)
    print('Encodings saved to file')

def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
















##############################################################################################################################
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.conf import settings
from django.db import IntegrityError
from .models import Attendance
import cv2
import numpy as np
import face_recognition
import os
import pickle
from datetime import datetime

class FaceRecognitionSystem:
    def __init__(self):
        self.path = settings.FACE_RECOGNITION_SETTINGS['TRAINING_PATH']
        self.encodings_file = os.path.join(settings.FACE_RECOGNITION_SETTINGS['ENCODINGS_PATH'], 'encodings.pkl')
        self.known_face_encodings = []
        self.known_names = []
        self.load_encodings()

    def load_encodings(self):
        if os.path.exists(self.encodings_file):
            with open(self.encodings_file, 'rb') as f:
                self.known_face_encodings, self.known_names = pickle.load(f)
            print(f"Loaded {len(self.known_names)} encodings from file")
        else:
            self.generate_encodings()

    def generate_encodings(self):
        images = []
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
                            print(f"Encoded {person_name}")
        
        if self.known_face_encodings:
            os.makedirs(os.path.dirname(self.encodings_file), exist_ok=True)
            with open(self.encodings_file, 'wb') as f:
                pickle.dump((self.known_face_encodings, self.known_names), f)

def mark_attendance_csv(name):
    csv_file = 'Attendance.csv'
    if not os.path.exists(csv_file):
        with open(csv_file, 'w') as f:
            f.write('Name,Time,Date\n')
    
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    time_string = now.strftime('%H:%M:%S')
    
    with open('attendance.csv', 'a', encoding='utf-8') as f:
        f.write(f'{name},{time_string},{date_string}\n')
    print(f"Marked attendance for {name} in CSV")

def is_attendance_marked(name, date):
    return Attendance.objects.filter(name=name, date=date).exists()

def reset_attendance_if_24_hours_passed(self):
    # Compare the current time with a stored timestamp
    # If more than 24 hours have passed, clear or reset attendance
    last_reset_path = os.path.join(settings.BASE_DIR, 'last_reset.txt')
    now = datetime.now()
    try:
        with open(last_reset_path, 'r') as f:
            last_reset_str = f.read().strip()
            last_reset_time = datetime.strptime(last_reset_str, '%Y-%m-%d %H:%M:%S')
            if (now - last_reset_time).total_seconds() >= 86400:  # 24 hours
                # Clear attendance file or DB entries here
                with open(last_reset_path, 'w') as reset_file:
                    reset_file.write(now.strftime('%Y-%m-%d %H:%M:%S'))
    except FileNotFoundError:
        # On first run, create the file
        with open(last_reset_path, 'w') as f:
            f.write(now.strftime('%Y-%m-%d %H:%M:%S'))

def mark_attendance(name):
    try:
        today = datetime.now().date()
        attendance, created = Attendance.objects.get_or_create(
            name=name,
            date=today,
            defaults={'time': datetime.now().time()}
        )
        return created
    except IntegrityError:
        return False

def gen_frames():
    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("Error: Could not open camera")
            return
            
        face_system = FaceRecognitionSystem()
        print("Camera initialized successfully")
        
        while True:
            success, img = camera.read()
            if not success:
                break

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                name = "Unknown"
                if face_system.known_face_encodings:
                    matches = face_recognition.compare_faces(face_system.known_face_encodings, encodeFace)
                    if True in matches:
                        faceDis = face_recognition.face_distance(face_system.known_face_encodings, encodeFace)
                        matchIndex = np.argmin(faceDis)
                        name = face_system.known_names[matchIndex].upper()
                        
                        today = datetime.now().date()
                        is_marked = is_attendance_marked(name, today)
                        
                        if not is_marked:
                            mark_attendance(name)
                            mark_attendance_csv(name)
                            status_color = (0, 255, 0)  # Green
                            status_text = f"{name} - Marked"
                        else:
                            status_color = (0, 255, 255)  # Yellow
                            status_text = f"{name} - Already Marked"
                else:
                    status_color = (0, 0, 255)  # Red
                    status_text = "Unknown"

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), status_color, 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), status_color, cv2.FILLED)
                cv2.putText(img, status_text, (x1+6, y2-6), 
                          cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except Exception as e:
        print(f"Error in gen_frames: {str(e)}")
    finally:
        if 'camera' in locals():
            camera.release()

def video_feed(request):
    return StreamingHttpResponse(gen_frames(),
                               content_type='multipart/x-mixed-replace; boundary=frame')

def mark_attendance_view(request):
    today = datetime.now().date()
    attendance = Attendance.objects.filter(date=today).order_by('-time')
    return render(request, 'attendance/mark_attendance.html', {'attendance': attendance})