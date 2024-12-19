import cv2
import numpy as np
import face_recognition
import os
import pickle
from datetime import datetime
from utils.face_detector import load_images, find_encodings
from utils.attendance_logger import log_attendance

path = 'training/Training_images'
images = []
classNames = []
encodeListKnown = []

# Load encodings from file if available
encodings_file = 'data/encodings.pkl'
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

    encodeListKnown = find_encodings(images)
    with open(encodings_file, 'wb') as f:
        pickle.dump((encodeListKnown, classNames), f)
    print('Encodings saved to file')

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert the image from BGR to RGB
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(encodeListKnown, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = classNames[best_match_index]

        # Log attendance
        log_attendance(name)

        # Draw a rectangle around the face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('Attendance System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()