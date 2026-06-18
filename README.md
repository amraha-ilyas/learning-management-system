# learning-management-system
A web-based Learning Management System (LMS) built with Python Flask, SQLite, HTML, and CSS. Features user authentication, assignment tracking, quiz management, score recording, and a student dashboard.

# Learning Management System (LMS)

## Overview

This project is a web-based Learning Management System (LMS) developed using Python Flask and SQLite. It provides a simple platform for students to manage assignments, take quizzes, and track their academic progress through an interactive dashboard.

The system includes user authentication, assignment management, quiz functionality, score tracking, and a clean dashboard interface.

## Features

* User Registration and Login
* Secure Session Management
* Student Dashboard
* Assignment Tracking
* Quiz Creation and Management
* Quiz Attempt System
* Score Recording
* Academic Schedule Display
* SQLite Database Integration
* Responsive User Interface

## Technologies Used

* Python
* Flask
* SQLite
* HTML5
* CSS3
* Jinja2 Templates

## Project Structure

```text
project/
│
├── app.py
├── database.db
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── assignments.html
│   ├── quizzes.html
│   ├── add_question.html
│   ├── take_quiz.html
│   └── quiz_result.html
│
└── static/
    └── css/
        └── style.css
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/lms-project.git
```

2. Navigate to the project folder

```bash
cd lms-project
```

3. Install Flask

```bash
pip install flask
```

4. Run the application

```bash
python app.py
```

5. Open your browser and visit

```text
http://127.0.0.1:5000
```

## Functionalities

### User Management

* Register a new account
* Login with existing credentials
* Session-based authentication

### Dashboard

* View assignment statistics
* View quiz statistics
* View academic schedule
* Access subjects and learning resources

### Quiz System

* Add quiz questions
* Attempt quizzes
* Automatic score calculation
* Result display after submission

### Assignment Management

* Track assignments
* Monitor completion status
* View pending and completed tasks

## Future Improvements

* Teacher/Admin Panel
* Subject-wise Quiz Management
* File Uploads for Assignments
* Attendance Tracking
* Notifications and Reminders
* Improved Analytics Dashboard

## Author

Developed as a university semester project using Flask and SQLite.
