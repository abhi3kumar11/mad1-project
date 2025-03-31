# Quiz Master - V1

## Overview
Quiz Master is a multi-user application designed for exam preparation, offering quizzes in multiple subjects and chapters. It supports two types of users: Admin and Regular Users. Admin users have full control over managing the platform, while Regular Users can register, log in, and attempt quizzes.

## Technologies Used
- **Backend**: Flask
- **Frontend**: HTML, CSS, Bootstrap, Jinja2 (templating)
- **Database**: SQLite
- **Form Handling**: WTForms
- **Authentication**: Flask-Login (for user login and session management)

## Features
- **Admin Login**: Pre-configured admin credentials for login.
- **Admin Dashboard**: Allows the admin to manage subjects, chapters, quizzes, and questions.
- **User Login**: Allows users to register and attempt quizzes.
- **Quiz Attempt**: Users can choose a subject, chapter, and attempt quizzes.
- **Score Tracking**: Tracks user scores and displays past attempts.

## Admin Login Instructions

1. **Pre-configured Admin Account**:  
   The application does not require the admin to register through the UI. Instead, the admin account is pre-configured when the database is initialized.  
   
   **Admin Credentials** (pre-set in the database):
   - **Username/Email**: `admin@quizmaster.com`  
   - **Password**: `adminpassword`  

2. **Login Procedure**:  
   - Open the application in your web browser by navigating to `http://127.0.0.1:5000` (or the relevant URL if deployed to a server).
   - On the home page or login page, you will see two login options: one for Admin and one for Users.
   
   - **For Admin Login**:
     - Enter the pre-configured **Admin Email** (`admin@gmail.com`).
     - Enter the **Password** (`admin_password`).
     - Click the **Login** button.
   
   - Upon successful login, you will be redirected to the **Admin Dashboard**, where you can manage subjects, chapters, quizzes, questions, and user statistics.

## User Instructions

1. **User Registration**:
   - Users must register an account with their email, full name, qualification, and date of birth.
   - After successful registration, users can log in to attempt quizzes.

2. **Attempt a Quiz**:
   - After logging in, users can choose from the list of available subjects and chapters.
   - They can attempt quizzes within the selected chapter.

3. **View Results**:
   - After completing a quiz, users can view their score and results.
   - The system also tracks their past attempts and displays them for review.

## Core Functionalities

- **Admin Features**:
  - Create, edit, and delete subjects, chapters, and quizzes.
  - Add, edit, or delete quiz questions.
  - View user statistics and quiz results.

- **User Features**:
  - Register and log in.
  - Attempt quizzes based on available subjects and chapters.
  - Track scores for past quiz attempts.

## Installation Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/abhi3kumar11/mad1-project.git
