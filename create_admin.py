#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/home/vishal/Desktop/student-manage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

# Setup Django
django.setup()

from academic.models import User

def create_admin_user():
    if not User.objects.filter(role='Admin').exists():
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='Admin',
            first_name='System',
            last_name='Administrator'
        )
        print('Admin user created: admin/admin123')
    else:
        print('Admin user already exists')

if __name__ == '__main__':
    create_admin_user()