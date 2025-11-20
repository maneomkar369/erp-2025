# Admin Credentials Management Guide

## 📋 Overview

This guide provides comprehensive instructions for creating and managing admin credentials in the Academic Portal system. The admin portal provides full system administration capabilities including user management, course management, announcements, and system reports.

## 🔐 Admin User Creation

### Method 1: Using Django Management Command (Recommended)

1. **Access Django Shell**
   ```bash
   python manage.py shell
   ```

2. **Create Admin User**
   ```python
   from academic.models import User

   # Create admin user
   admin = User.objects.create_user(
       username='admin',
       email='admin@example.com',
       password='your_secure_password',
       role='Admin',
       first_name='System',
       last_name='Administrator'
   )

   print(f"Admin user created: {admin.username}")
   ```

3. **Exit Django Shell**
   ```python
   exit()
   ```

### Method 2: Using Python Script

Create a file named `create_admin.py` with the following content:

```python
#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
django.setup()

from academic.models import User

def create_admin_user():
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")

    if User.objects.filter(username=username).exists():
        print("❌ Admin user already exists!")
        return

    try:
        admin = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='Admin',
            first_name=first_name,
            last_name=last_name
        )
        print(f"✅ Admin user '{username}' created successfully!")
        print(f"📧 Email: {email}")
        print("🔑 Role: Admin"
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == '__main__':
    create_admin_user()
```

Run the script:
```bash
python create_admin.py
```

### Method 3: Using Django Admin Interface

1. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

2. **Update User Role**
   ```python
   # In Django shell
   from academic.models import User
   user = User.objects.get(username='your_superuser')
   user.role = 'Admin'
   user.save()
   ```

## 🔑 Default Admin Credentials

For development/testing purposes, the following credentials are commonly used:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

⚠️ **Security Warning**: Change these default credentials in production!

## 🛠️ Admin Portal Features

Once logged in to the admin portal (`/portal-admin/login/`), you can:

### User Management
- Create new users (Students, Teachers, Admins)
- Edit user profiles and information
- Deactivate/reactivate user accounts
- Reset user passwords
- View user activity and statistics

### Course Management
- Create and manage courses
- Assign teachers to courses
- Manage course enrollments
- Update course materials and syllabus
- View course statistics

### Announcements
- Create system-wide announcements
- Target specific user groups
- Schedule announcements
- Track announcement delivery

### Reports & Analytics
- System usage statistics
- User registration trends
- Course enrollment reports
- Performance analytics
- Attendance summaries

## 🔒 Security Best Practices

### Password Requirements
- Minimum 8 characters
- Mix of uppercase and lowercase letters
- Include numbers and special characters
- Avoid common passwords

### Account Security
- Use strong, unique passwords
- Enable two-factor authentication (if implemented)
- Regularly rotate admin credentials
- Monitor login attempts and suspicious activity

### Session Management
- Set appropriate session timeouts
- Use secure cookies (HTTPS in production)
- Implement proper logout mechanisms

## 🚨 Troubleshooting

### Common Issues

**"Admin user already exists"**
- Check existing users: `User.objects.filter(role='Admin')`
- Use a different username or delete existing admin

**"Permission denied"**
- Ensure you're running commands with proper permissions
- Check if virtual environment is activated

**"Module not found"**
- Verify Django settings module path
- Ensure all dependencies are installed

**"Database connection failed"**
- Check database configuration in `settings.py`
- Ensure database server is running
- Run migrations: `python manage.py migrate`

### Resetting Admin Password

```python
from academic.models import User
from django.contrib.auth.hashers import make_password

admin = User.objects.get(username='admin')
admin.password = make_password('new_password')
admin.save()
print("Password updated successfully")
```

### Checking Admin Users

```python
from academic.models import User

# List all admin users
admins = User.objects.filter(role='Admin')
for admin in admins:
    print(f"Username: {admin.username}, Email: {admin.email}, Active: {admin.is_active}")
```

## 📞 Support

If you encounter issues with admin credential creation or management:

1. Check the Django logs for error messages
2. Verify database connectivity
3. Ensure all migrations are applied
4. Review the troubleshooting section above

For additional support, refer to the main project documentation or create an issue in the project repository.