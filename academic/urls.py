from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portal-admin/login/', views.admin_login, name='admin_login'),
    path('portal-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('portal-admin/users/', views.admin_users, name='admin_users'),
    path('portal-admin/courses/', views.admin_courses, name='admin_courses'),
    path('portal-admin/announcements/', views.admin_announcements, name='admin_announcements'),
    path('portal-admin/reports/', views.admin_reports, name='admin_reports'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('student/login/', views.student_login, name='student_login'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher/results/', views.teacher_results, name='teacher_results'),
    path('teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('teacher/assignments/', views.teacher_assignments, name='teacher_assignments'),
    path('teacher/course/<int:course_id>/', views.teacher_course_detail, name='teacher_course_detail'),
    path('student/results/', views.student_results, name='student_results'),
    path('student/analytics/', views.student_analytics, name='student_analytics'),
    path('student/assignments/', views.student_assignments, name='student_assignments'),
    path('student/attendance/', views.student_attendance, name='student_attendance'),
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    path('student/profile/', views.student_profile, name='student_profile'),
]