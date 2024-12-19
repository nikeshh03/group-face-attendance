# README.md

# Attendance System

This project implements a face detection application to mark attendance using facial recognition technology. It utilizes various utility modules for face detection, attendance logging, and image processing.

## Project Structure

```
attendance-system
├── src
│   ├── main.py                # Entry point of the application
│   ├── utils                  # Utility modules for the application
│   │   ├── face_detector.py    # Functions for detecting faces in images
│   │   ├── attendance_logger.py # Functions for logging attendance data
│   │   └── image_processor.py   # Functions for image processing tasks
│   ├── data                   # Directory for data files
│   │   └── encodings.pkl      # Stores face encodings and associated names
│   └── training               # Directory for training images
│       └── Training_images    # Subdirectories of training images for individuals
├── tests                      # Directory for test files
│   └── test_face_detector.py   # Unit tests for face detection functionality
├── requirements.txt           # Lists project dependencies
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd attendance-system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Prepare the training images by placing them in the `src/training/Training_images` directory, organized by individual names.

4. Run the application:
   ```
   python src/main.py
   ```

## Usage

- The application will detect faces from the training images and mark attendance based on recognized faces.
- Attendance records will be logged and can be accessed as needed.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.