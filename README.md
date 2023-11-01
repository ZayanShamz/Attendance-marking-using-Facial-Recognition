# Academic Attendance Web Application using Face Recognition

This web application is designed for academic institutions to streamline attendance recording through the use of face recognition technology.

## Features

### Administrator
- **Manage Faculty and Classes:** Administrators can add and manage faculty members and classes within the system.
- **Add Students to Classes:** Administrators can assign students to specific classes.
- **View and Remove Entries:** Administrators have the capability to view and remove faculty, class, and student entries.

### Faculty
- **Faculty Login:** Faculty members can log in to the system using their credentials.
- **Manage Students:** Faculty can add students to their respective classes.
- **View Students:** Faculty can view the list of students enrolled in their class.
- **Take Attendance by Face Recognition:** Faculty can use the face recognition feature to mark student attendance.
- **Submit Attendance Records:** After taking attendance, faculty members can submit the attendance records for their class.
- **View Attendance Records:** Faculty can also access and review attendance records.

## Technology Stack

- **Programming Language:** Python
- **Framework:** Flask
- **Database:** MySQL
- **Face Recognition Software:** deepface

## Python Requirements

To run the application, ensure you have the following Python packages installed:

- **Python:** 3.10.7
- **TensorFlow:** 2.11.0
- **Keras:** 2.11.0
- **dlib:** 19.22.99 (file included)
- **Matplotlib**
- **OpenCV-Python:** 4.5.5.64
- **Pandas:** 1.5.3

## Getting Started

1. Install Python and the required packages mentioned above.
2. Set up a MySQL database to store faculty, class, student, and attendance records.
3. Clone this repository.
4. Configure the database connection in your Flask application.
5. Run the Flask application to start the web server.

## Usage

1. As an administrator, add faculty and classes, assign students to classes, and manage entries.
2. Faculty members can log in, add students to their classes, take attendance using face recognition, and submit records.
3. Both administrators and faculty can view attendance records.

Please refer to the documentation or help guide for detailed instructions on how to set up and use the application.
