# SmartTrack: Face Recognition Attendance System

## Overview
SmartTrack is an AI-powered face recognition attendance system designed to streamline and automate the process of tracking attendance. The system integrates with a Django backend, uses OpenCV for real-time face detection, and provides a user-friendly dashboard for monitoring and reporting attendance data.

## Features
- **User Authentication:** Secure login and registration for users.
- **Real-Time Face Detection:** Live video feed for face detection and recognition.
- **Attendance Tracking:** Automatically mark attendance for recognized faces.
- **Reporting System:** Generate daily attendance reports.
- **Reset Mechanism:** Automatically resets attendance records every 24 hours.

---

## System Architecture
1. **Frontend**: User-friendly interface for live camera feed and dashboard.
2. **Backend**: Django-powered backend with robust data handling and APIs.
3. **Face Recognition Core**: Uses OpenCV and face_recognition library for real-time recognition.
4. **Database**: SQLite (default) or PostgreSQL for attendance records and user management.
5. **Reports**: Attendance logs and CSV generation.

---

## Project Structure
```
smarttrack/
├── manage.py
├── requirements.txt
├── static/
│   ├── css/
│   └── js/
├── media/
│   └── training_images/
├── templates/
├── user/
├── dashboard/
└── attendance/
```

### Key Directories
- **`media/training_images/`**: Folder to store images for training face recognition.
- **`templates/`**: HTML templates for frontend views.
- **`attendance/`**: App for handling attendance logic.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Virtual environment
- Webcam access
- Database (SQLite/PostgreSQL)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/username/smarttrack.git
   cd smarttrack
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database in `settings.py`.
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Face Recognition Setup
1. Add training images in `media/training_images/` directory.
2. Each person should have a folder with their name containing their images.
3. Start encoding the training images:
   ```bash
   python manage.py encode_faces
   ```

---

## Core Functionalities

### Live Camera Feed
- Accessed via `/video_feed/` endpoint.
- Displays a live feed with real-time face detection and recognition.

### Attendance Marking
- Automatically marks attendance for recognized individuals.
- Logs attendance in the database and a CSV file.

### Dashboard
- View daily attendance records.
- Accessible via `/attendance/` endpoint.

---

## Security Measures
- Firebase Authentication for user login.
- Face encoding encryption for secure data storage.
- CSRF protection in Django.
- Session security to prevent hijacking.

---


## Future Enhancements
- Add multi-camera support.
- Integrate advanced analytics for attendance trends.
- Support for mobile apps.

---

## Authors
Developed by @nikeshh03 and contributors.
