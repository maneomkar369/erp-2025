📘 Academic Portal — Teacher & Student Login System (Django Framework)

## 🚀 Quick Setup Guide

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/maneomkar369/erp-2025.git
   cd erp-2025
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user**
   ```bash
   # Option 1: Using Django shell
   python manage.py shell -c "from academic.models import User; User.objects.create_user(username='admin', email='admin@example.com', password='admin123', role='Admin', first_name='System', last_name='Administrator')"

   # Option 2: Follow detailed guide
   # See ADMIN_GUIDE.md for comprehensive admin setup instructions
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver 8001
   ```

7. **Access the application**
   - Main portal: http://127.0.0.1:8001/
   - Admin portal: http://127.0.0.1:8001/portal-admin/login/
   - Admin credentials: `admin` / `admin123`

### Features Overview
- **Teacher Portal**: Manage courses, students, grades, and attendance
- **Student Portal**: View results, attendance, and course materials
- **Admin Portal**: Full system administration and user management

### 📚 Documentation
- **[Admin Guide](ADMIN_GUIDE.md)**: Comprehensive guide for creating and managing admin credentials
- **API Documentation**: REST API endpoints (coming soon)
- **Deployment Guide**: Production deployment instructions (coming soon)
- **Admin Portal**: Full system administration and user management

---

This document provides a complete technical specification for building a Teacher & Student Login System using the Django Framework. It includes detailed explanations of system pages, workflows, features, and backend structure.

🏗️ 1. Project Overview

This portal provides separate login sections for Teachers and Students. Each user type gets their own dashboard with specific functionalities such as:

Viewing and managing student performance

Uploading grades

Accessing course materials

Viewing exam results, attendance, analytics, etc.

The full system is built using Django (Python) with secure authentication flows.

🧰 2. Tech Stack (Django Framework)
Backend

Python 3.x

Django Framework

Django ORM for database operations

SQLite / PostgreSQL / MySQL

Django Authentication System (Custom user model for Teacher/Student roles)

Django Messages Framework for notifications and error messages

Django REST Framework (optional) for API integration

Frontend

HTML5 / CSS3 / JavaScript

Bootstrap / TailwindCSS (any responsive UI library)

Security

Django’s built-in password hashing

CSRF Protection

Optional: Captcha, 2FA, Email OTP

📁 3. Folder / App Structure (Recommended)
├── project_root/
│   ├── manage.py
│   ├── portal/ (main Django app)
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── templates/
│   │   │   ├── teacher/
│   │   │   ├── student/
│   │   │   ├── login_pages/
│   │   │   ├── dashboard_pages/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   ├── images/
🧑‍🏫 4. Teacher Login Section
🎯 Purpose

Teachers log in to manage student results, view courses, upload grades, send announcements, and track attendance.

🔑 4.1 Teacher Login Page Features
Login Form Inputs

Username / Email

Password

Remember Me (optional)

Forgot Password link

Authentication Flow

Teacher enters credentials.

Django checks:

User exists

User role = Teacher

Account is active

If any mismatch → Error message is shown.

Error Messages

"Invalid username or password."

"Your account has not been activated. Contact admin."

Security

Captcha (optional)

2FA via Email/SMS (optional)

Post Login Redirect

→ Teacher Dashboard

🖥️ 5. Teacher Dashboard Features
📚 Assigned Courses

List of all courses teacher handles

Ability to:

Update course material

Upload files

Update syllabus

📝 Student List

View enrolled students

Search / Filter students

📊 Results Management

Enter grades manually

Update marks

Upload bulk marks (CSV/Excel)

View analytics:

Average scores

Performance trends

Graphs and charts

📢 Communication Tools

Send announcements to all students

Notify specific student groups

Feedback submission options

🕒 Attendance Management

Mark daily attendance

View attendance history

Generate attendance reports

🔐 Logout

Secure session termination → Redirect to login page.

🎓 6. Student Login Section
🎯 Purpose

Students log in to view academic performance, grades, attendance, and exam results.

🔑 6.1 Student Login Page Features
Login Form Inputs

Student ID / Email

Password

Remember Me

Forgot Password

Error Messages

"Incorrect student ID or password."

"Account inactive. Contact admin."

Security

Captcha

2FA (optional)

Post Login Redirect

→ Student Dashboard

🖥️ 7. Student Dashboard Features
📄 View Results

Semester-wise marks

Internal & final exam results

Downloadable mark sheets

📉 Performance Analytics

Graphs showing performance trends

Subject-wise comparison

Rank comparison

📝 Assignments & Materials

Download assignments

Upload assignment submissions

View feedback

🕒 Attendance

View percentage attendance

Monthly attendance charts

🔐 Logout**

End session → Redirect to login page.

🧱 8. Database Schema (Django Models)
User Model (AbstractBaseUser)

id

username

email

password

role (Teacher / Student)

is_active

date_joined

Teacher Model

user (OneToOne)

department

qualifications

Student Model

user (OneToOne)

roll_no

class

batch

Course Model

course_code

course_name

assigned_teacher

Results Model

student

course

marks

exam_type

Attendance Model

student

course

date

status

🚀 9. Future Enhancements

Online exams module

AI-based performance prediction

Push notifications

Mobile app integration (React Native / Flutter)