# Face Attendance Marking and Management System

## 📖 Project Overview

The **Face Attendance Marking and Management System** is a real-time facial recognition-based attendance solution. It identifies multiple employees standing in front of a camera and differentiates between employees and non-employees. The system is lightweight, user-friendly, and integrates seamlessly with Firebase for authentication, data storage, and management.

---

## 🎯 Purpose

The goal of this project is to automate the attendance marking process using advanced face recognition technology. This system:
- Saves time for employees and administrators.
- Minimizes errors from manual attendance processes.
- Provides a centralized, secure, and real-time attendance management solution.

---

## ✨ Features

- **Face Detection and Recognition**  
  - Detects and identifies multiple faces in real-time.  
  - Differentiates between employees and non-employees.

- **Admin Panel**  
  - Manage employee profiles and attendance records.  
  - View and download attendance logs.

- **Real-time Feedback**  
  - Displays attendance remarks instantly on a webpage.

- **Firebase Integration**  
  - **Authentication**: Supports email/password login and Google OAuth.  
  - **Realtime Database**: Stores attendance records with real-time updates.  
  - **Cloud Storage**: Handles employee profile images and related files.

- **Automated Camera Management**  
  - Automatically shuts down the camera after 1 minute of inactivity.

- **Lightweight Frontend**  
  - Built with HTML, CSS, and JavaScript for a responsive and clean UI.

---

## 🚀 How to Run the Project

### Prerequisites
1. Python (Version 3.8 or higher)
2. Flask Framework
3. Firebase Project (Configured for Authentication, Storage, and Realtime Database)
4. Python libraries (listed in `requirements.txt`)

### Steps to Run

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-repo/face-attendance-system.git
   cd face-attendance-system
2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
3. **Set Up Firebase**
    Create a Firebase project and enable:
    Authentication (email/password and Google OAuth)
    Realtime Database
    Cloud Storage
        Download the Firebase Admin SDK credentials and place them in the project directory (e.g., firebase-adminsdk.json).
4. **Configure Environment Variables**
    Create a .env file in the root directory.
    ```bash 
        FLASK_APP=app.py
    FLASK_ENV=development
    FIREBASE_CONFIG_PATH=path/to/firebase-adminsdk.json
5. **Start the Server**
    ```bash
        flask run