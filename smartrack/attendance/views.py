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
from datetime import datetime, timedelta

class FaceRecognitionSystem:
    def __init__(self):
        self.training_path = settings.FACE_RECOGNITION_SETTINGS['TRAINING_PATH']
        self.encodings_file = os.path.join(settings.FACE_RECOGNITION_SETTINGS['ENCODINGS_PATH'], 'encodings.pkl')
        self.known_face_encodings = []
        self.known_names = []
        self.load_encodings()

    def load_encodings(self):
        if os.path.exists(self.encodings_file):
            with open(self.encodings_file, 'rb') as f:
                self.known_face_encodings, self.known_names = pickle.load(f)
            print(f"Loaded {len(self.known_names)} encodings from file.")
        else:
            self.generate_encodings()

    def generate_encodings(self):
        for person_name in os.listdir(self.training_path):
            person_path = os.path.join(self.training_path, person_name)
            if os.path.isdir(person_path):
                for img_name in os.listdir(person_path):
                    img_path = os.path.join(person_path, img_name)
                    img = cv2.imread(img_path)
                    if img is not None:
                        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        face_encodings = face_recognition.face_encodings(rgb_img)
                        if face_encodings:
                            self.known_face_encodings.append(face_encodings[0])
                            self.known_names.append(person_name)
                            print(f"Encoded {person_name}.")

        if self.known_face_encodings:
            os.makedirs(os.path.dirname(self.encodings_file), exist_ok=True)
            with open(self.encodings_file, 'wb') as f:
                pickle.dump((self.known_face_encodings, self.known_names), f)


def initialize_csv():
    csv_file = 'Attendance.csv'
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write('Name,Time,Date\n')
    return csv_file


def mark_attendance_csv(name):
    csv_file = initialize_csv()
    now = datetime.now()
    with open(csv_file, 'a', encoding='utf-8') as f:
        f.write(f"{name},{now.strftime('%H:%M:%S')},{now.strftime('%Y-%m-%d')}\n")
    print(f"Marked attendance for {name} in CSV.")


def is_attendance_marked(name, date):
    return Attendance.objects.filter(name=name, date=date).exists()


def mark_attendance(name):
    today = datetime.now().date()
    try:
        attendance, created = Attendance.objects.get_or_create(
            name=name,
            date=today,
            defaults={'time': datetime.now().time()}
        )
        if created:
            print(f"Marked attendance for {name} in database.")
        return created
    except IntegrityError:
        print(f"Error marking attendance for {name}.")
        return False


def reset_attendance_if_needed():
    reset_file = os.path.join(settings.BASE_DIR, 'last_reset.txt')
    now = datetime.now()
    try:
        if os.path.exists(reset_file):
            with open(reset_file, 'r') as f:
                last_reset_time = datetime.strptime(f.read().strip(), '%Y-%m-%d %H:%M:%S')
            if (now - last_reset_time) >= timedelta(days=1):
                Attendance.objects.all().delete()
                print("Attendance records cleared after 24 hours.")
        with open(reset_file, 'w') as f:
            f.write(now.strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        print(f"Error in resetting attendance: {str(e)}")


def gen_frames():
    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("Error: Could not open camera.")
            return

        face_system = FaceRecognitionSystem()
        print("Camera initialized successfully.")

        while True:
            success, img = camera.read()
            if not success:
                break

            small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "Unknown"

                if face_system.known_face_encodings:
                    matches = face_recognition.compare_faces(face_system.known_face_encodings, face_encoding, tolerance=0.5)
                    face_distances = face_recognition.face_distance(face_system.known_face_encodings, face_encoding)

                    if True in matches:
                        best_match_index = np.argmin(face_distances)
                        name = face_system.known_names[best_match_index]

                        today = datetime.now().date()
                        if not is_attendance_marked(name, today):
                            mark_attendance(name)
                            mark_attendance_csv(name)

                # Scale face locations back to original frame size
                top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4

                # Draw face box and label
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(img, (left, top), (right, bottom), color, 2)
                cv2.rectangle(img, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(img, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)

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
    reset_attendance_if_needed()
    return StreamingHttpResponse(gen_frames(),
                                  content_type='multipart/x-mixed-replace; boundary=frame')


def mark_attendance_view(request):
    today = datetime.now().date()
    attendance_records = Attendance.objects.filter(date=today).order_by('-time')
    return render(request, 'mark_attendance.html', {'attendance': attendance_records})