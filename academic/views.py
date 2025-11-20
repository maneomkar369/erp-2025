from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Avg
from .models import User, Teacher, Student, Course, Results, Attendance, Announcement, CourseFile, Assignment, Submission

def home(request):
    return render(request, 'academic/home.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role == 'Admin':
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin.')
    return render(request, 'academic/admin_login.html')

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role == 'Teacher':
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a teacher.')
    return render(request, 'academic/teacher_login.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role == 'Student':
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a student.')
    return render(request, 'academic/student_login.html')

def teacher_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'Teacher':
        return redirect('teacher_login')
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(assigned_teacher=teacher)
    students = Student.objects.all()
    results = Results.objects.filter(course__in=courses)
    attendance = Attendance.objects.filter(course__in=courses)
    announcements = Announcement.objects.filter(teacher=teacher)

    # Prepare student data with results
    student_data = []
    for student in students:
        data = {
            'id': student.id,
            'roll_no': student.roll_no,
            'name': student.user.username,
            'class_name': student.class_name,
            'results': {},
            'attendance_perc': 85,  # Placeholder, calculate properly
        }
        student_results = results.filter(student=student)
        for result in student_results:
            if result.exam_type == 'CA-I':
                data['results']['cai'] = {'marks': result.marks, 'date': result.date}
            elif result.exam_type == 'MSE':
                data['results']['mse'] = {'marks': result.marks, 'date': result.date}
            elif result.exam_type == 'CA-II':
                data['results']['caii'] = {'marks': result.marks, 'date': result.date}
        # Calculate overall grade
        marks_list = [float(r['marks']) for r in data['results'].values()]
        if marks_list:
            avg = sum(marks_list) / len(marks_list)
            if avg >= 90:
                grade = 'A'
            elif avg >= 80:
                grade = 'B'
            elif avg >= 70:
                grade = 'C'
            elif avg >= 60:
                grade = 'D'
            else:
                grade = 'F'
        else:
            grade = 'N/A'
        data['grade'] = grade
        student_data.append(data)

    if request.method == 'POST':
        if 'enter_result' in request.POST:
            student_id = request.POST['student']
            course_id = request.POST['course']
            marks = request.POST['marks']
            exam_type = request.POST['exam_type']
            date = request.POST.get('date')
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            Results.objects.create(student=student, course=course, marks=marks, exam_type=exam_type, date=date)
            messages.success(request, 'Result entered successfully.')
        elif 'mark_attendance' in request.POST:
            student_id = request.POST['student']
            course_id = request.POST['course']
            date = request.POST['date']
            status = request.POST['status']
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            Attendance.objects.create(student=student, course=course, date=date, status=status)
            messages.success(request, 'Attendance marked successfully.')
        elif 'send_announcement' in request.POST:
            message = request.POST['message']
            Announcement.objects.create(teacher=teacher, message=message)
            messages.success(request, 'Announcement sent successfully.')
        return redirect('teacher_dashboard')
    context = {
        'courses': courses,
        'student_data': student_data,
        'results': results,
        'attendance': attendance,
        'announcements': announcements,
    }
    return render(request, 'academic/teacher_dashboard.html', context)

def student_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'Student':
        return redirect('student_login')
    student = Student.objects.get(user=request.user)
    results = Results.objects.filter(student=student).select_related('course')
    attendance = Attendance.objects.filter(student=student).select_related('course')
    # For demo, get all assignments; in real, filter by student's courses
    assignments = Assignment.objects.all()
    submissions = Submission.objects.filter(student=student)
    # Calculate attendance percentage
    total_att = attendance.count()
    present = attendance.filter(status='Present').count()
    att_perc = (present / total_att * 100) if total_att > 0 else 0
    # Group results
    internal_results = results.filter(exam_type__in=['CA-I', 'CA-II'])
    final_results = results.filter(exam_type='MSE')
    # Calculate averages
    avg_internal = internal_results.aggregate(avg=Avg('marks'))['avg'] or 0
    avg_final = final_results.aggregate(avg=Avg('marks'))['avg'] or 0
    if request.method == 'POST' and 'submit_assignment' in request.POST:
        assignment_id = request.POST['submit_assignment']
        file = request.FILES.get('file')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        Submission.objects.create(student=student, assignment=assignment, file=file)
        messages.success(request, 'Assignment submitted successfully.')
        return redirect('student_dashboard')
    context = {
        'student': student,
        'results': results,
        'internal_results': internal_results,
        'final_results': final_results,
        'attendance': attendance,
        'assignments': assignments,
        'submissions': submissions,
        'att_perc': att_perc,
        'avg_internal': avg_internal,
        'avg_final': avg_final,
    }
    return render(request, 'academic/student_dashboard.html', context)

def student_results(request):
    if not request.user.is_authenticated or request.user.role != 'Student':
        return redirect('student_login')
    student = Student.objects.get(user=request.user)
    results = Results.objects.filter(student=student).select_related('course')
    # Group results
    internal_results = results.filter(exam_type__in=['CA-I', 'CA-II'])
    final_results = results.filter(exam_type='MSE')
    context = {
        'student': student,
        'internal_results': internal_results,
        'final_results': final_results,
    }
    return render(request, 'academic/student_results.html', context)

def student_analytics(request):
    if not request.user.is_authenticated or request.user.role != 'Student':
        return redirect('student_login')
    student = Student.objects.get(user=request.user)
    results = Results.objects.filter(student=student).select_related('course')
    # Group results
    internal_results = results.filter(exam_type__in=['CA-I', 'CA-II'])
    final_results = results.filter(exam_type='MSE')
    # Calculate averages
    avg_internal = internal_results.aggregate(avg=Avg('marks'))['avg'] or 0
    avg_final = final_results.aggregate(avg=Avg('marks'))['avg'] or 0
    # Calculate overall average
    overall_avg = (avg_internal + avg_final) / 2 if (avg_internal + avg_final) > 0 else 0
    context = {
        'student': student,
        'avg_internal': avg_internal,
        'avg_final': avg_final,
        'overall_avg': overall_avg,
    }
    return render(request, 'academic/student_analytics.html', context)

def student_assignments(request):
    if not request.user.is_authenticated or request.user.role != 'Student':
        return redirect('student_login')
    student = Student.objects.get(user=request.user)
    # For demo, get all assignments; in real, filter by student's courses
    assignments = Assignment.objects.all()
    submissions = Submission.objects.filter(student=student)
    # Calculate pending assignments (assignments not submitted by this student)
    submitted_assignment_ids = submissions.values_list('assignment_id', flat=True)
    pending_assignments = assignments.exclude(id__in=submitted_assignment_ids)
    pending_count = pending_assignments.count()
    if request.method == 'POST' and 'submit_assignment' in request.POST:
        assignment_id = request.POST['submit_assignment']
        file = request.FILES.get('file')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        Submission.objects.create(student=student, assignment=assignment, file=file)
        messages.success(request, 'Assignment submitted successfully.')
        return redirect('student_assignments')
    context = {
        'student': student,
        'assignments': assignments,
        'submissions': submissions,
        'pending_count': pending_count,
    }
    return render(request, 'academic/student_assignments.html', context)

def student_attendance(request):
    if not request.user.is_authenticated or request.user.role != 'Student':
        return redirect('student_login')
    student = Student.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student=student).select_related('course')
    # Calculate attendance percentage
    total_att = attendance.count()
    present = attendance.filter(status='Present').count()
    att_perc = (present / total_att * 100) if total_att > 0 else 0
    context = {
        'student': student,
        'attendance': attendance,
        'att_perc': att_perc,
    }
    return render(request, 'academic/student_attendance.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def teacher_results(request):
    if not request.user.is_authenticated or request.user.role != 'Teacher':
        return redirect('teacher_login')
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(assigned_teacher=teacher)
    students = Student.objects.all()
    results = Results.objects.filter(course__in=courses)
    student_data = []
    for student in students:
        data = {
            'id': student.id,
            'roll_no': student.roll_no,
            'name': student.user.username,
            'class_name': student.class_name,
            'results': {},
        }
        student_results = results.filter(student=student)
        for result in student_results:
            if result.exam_type == 'CA-I':
                data['results']['cai'] = {'marks': result.marks, 'date': result.date}
            elif result.exam_type == 'MSE':
                data['results']['mse'] = {'marks': result.marks, 'date': result.date}
            elif result.exam_type == 'CA-II':
                data['results']['caii'] = {'marks': result.marks, 'date': result.date}
        marks_list = [float(r['marks']) for r in data['results'].values()]
        if marks_list:
            avg = sum(marks_list) / len(marks_list)
            if avg >= 90:
                grade = 'A'
            elif avg >= 80:
                grade = 'B'
            elif avg >= 70:
                grade = 'C'
            elif avg >= 60:
                grade = 'D'
            else:
                grade = 'F'
        else:
            grade = 'N/A'
        data['grade'] = grade
        student_data.append(data)
    context = {'student_data': student_data}
    return render(request, 'academic/teacher_results.html', context)

def teacher_attendance(request):
    if not request.user.is_authenticated or request.user.role != 'Teacher':
        return redirect('teacher_login')
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(assigned_teacher=teacher)
    students = Student.objects.all()
    attendance = Attendance.objects.filter(course__in=courses)
    context = {'students': students, 'attendance': attendance}
    return render(request, 'academic/teacher_attendance.html', context)

def teacher_course_detail(request, course_id):
    if not request.user.is_authenticated or request.user.role != 'Teacher':
        return redirect('teacher_login')
    course = get_object_or_404(Course, id=course_id, assigned_teacher__user=request.user)
    if request.method == 'POST':
        if 'update_material' in request.POST:
            material = request.POST['material']
            course.material = material
            course.save()
            messages.success(request, 'Course material updated successfully.')
        elif 'update_syllabus' in request.POST:
            syllabus = request.POST['syllabus']
            course.syllabus = syllabus
            course.save()
            messages.success(request, 'Syllabus updated successfully.')
        elif 'upload_file' in request.POST and request.FILES.get('file'):
            file = request.FILES['file']
            CourseFile.objects.create(course=course, file=file)
            messages.success(request, 'File uploaded successfully.')
        return redirect('teacher_course_detail', course_id=course.id)
    files = CourseFile.objects.filter(course=course)
    context = {'course': course, 'files': files}
    return render(request, 'academic/teacher_course_detail.html', context)

def teacher_assignments(request):
    if not request.user.is_authenticated or request.user.role != 'Teacher':
        return redirect('teacher_login')
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(assigned_teacher=teacher)
    
    if request.method == 'POST':
        if 'create_assignment' in request.POST:
            course_id = request.POST['course']
            title = request.POST['title']
            description = request.POST['description']
            due_date = request.POST['due_date']
            file = request.FILES.get('file')
            course = Course.objects.get(id=course_id, assigned_teacher=teacher)
            Assignment.objects.create(
                course=course,
                title=title,
                description=description,
                due_date=due_date,
                file=file
            )
            messages.success(request, 'Assignment created successfully.')
        elif 'grade_submission' in request.POST:
            submission_id = request.POST['submission_id']
            feedback = request.POST['feedback']
            status = request.POST['status']
            submission = Submission.objects.get(id=submission_id, assignment__course__assigned_teacher=teacher)
            submission.feedback = feedback
            submission.status = status
            submission.save()
            messages.success(request, 'Submission graded successfully.')
        return redirect('teacher_assignments')
    
    assignments = Assignment.objects.filter(course__in=courses).select_related('course').prefetch_related('submissions__student__user')
    context = {
        'courses': courses,
        'assignments': assignments,
    }
    return render(request, 'academic/teacher_assignments.html', context)

def teacher_profile(request):
    if not request.user.is_authenticated or request.user.role != 'Teacher':
        return redirect('teacher_login')
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(assigned_teacher=teacher)
    total_students = Student.objects.count()
    total_assignments = Assignment.objects.filter(course__in=courses).count()
    total_submissions = Submission.objects.filter(assignment__course__in=courses).count()

    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()

        # Update teacher information
        teacher.department = request.POST.get('department', '').strip()
        teacher.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('teacher_profile')

    context = {
        'teacher': teacher,
        'courses': courses,
        'total_students': total_students,
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
    }
    return render(request, 'academic/teacher_profile.html', context)

def student_profile(request):
    if not request.user.is_authenticated or request.user.role != 'Student':
        return redirect('student_login')
    student = Student.objects.get(user=request.user)
    results = Results.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)
    submissions = Submission.objects.filter(student=student)

    # Calculate attendance percentage
    total_att = attendance.count()
    present = attendance.filter(status='Present').count()
    att_perc = (present / total_att * 100) if total_att > 0 else 0

    # Calculate average marks
    marks_list = [float(result.marks) for result in results]
    avg_marks = sum(marks_list) / len(marks_list) if marks_list else 0

    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()

        # Update student information
        if request.POST.get('date_of_birth'):
            try:
                student.date_of_birth = request.POST.get('date_of_birth')
            except ValueError:
                pass  # Keep existing date if invalid
        student.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('student_profile')

    context = {
        'student': student,
        'results': results,
        'attendance': attendance,
        'submissions': submissions,
        'att_perc': att_perc,
        'avg_marks': avg_marks,
        'total_results': results.count(),
        'total_submissions': submissions.count(),
    }
    return render(request, 'academic/student_profile.html', context)

def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('admin_login')

    # System statistics
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_assignments = Assignment.objects.count()
    total_submissions = Submission.objects.count()
    total_results = Results.objects.count()
    total_announcements = Announcement.objects.count()

    # Recent activities
    recent_students = Student.objects.order_by('-user__date_joined')[:5]
    recent_teachers = Teacher.objects.order_by('-joining_date')[:5]
    recent_announcements = Announcement.objects.order_by('-date')[:5]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
        'total_results': total_results,
        'total_announcements': total_announcements,
        'recent_students': recent_students,
        'recent_teachers': recent_teachers,
        'recent_announcements': recent_announcements,
    }
    return render(request, 'academic/admin_dashboard.html', context)

def admin_users(request):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('admin_login')

    if request.method == 'POST':
        if 'create_user' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            role = request.POST['role']
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role,
                    first_name=first_name,
                    last_name=last_name
                )

                if role == 'Teacher':
                    employee_id = request.POST.get('employee_id', f'T{user.id:03d}')
                    department = request.POST.get('department', 'General')
                    Teacher.objects.create(
                        user=user,
                        employee_id=employee_id,
                        department=department
                    )
                elif role == 'Student':
                    roll_no = request.POST.get('roll_no', f'S{user.id:03d}')
                    class_name = request.POST.get('class_name', 'General')
                    batch = request.POST.get('batch', '2024')
                    Student.objects.create(
                        user=user,
                        roll_no=roll_no,
                        class_name=class_name,
                        batch=batch
                    )

                messages.success(request, f'{role} created successfully.')
                return redirect('admin_users')

        elif 'delete_user' in request.POST:
            user_id = request.POST['user_id']
            user = get_object_or_404(User, id=user_id)
            if user.role != 'Admin':  # Prevent deleting admin users
                user.delete()
                messages.success(request, 'User deleted successfully.')
            else:
                messages.error(request, 'Cannot delete admin users.')
            return redirect('admin_users')

    users = User.objects.all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'academic/admin_users.html', context)

def admin_courses(request):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('admin_login')

    if request.method == 'POST':
        if 'create_course' in request.POST:
            course_code = request.POST['course_code']
            course_name = request.POST['course_name']
            teacher_id = request.POST['teacher']

            if Course.objects.filter(course_code=course_code).exists():
                messages.error(request, 'Course code already exists.')
            else:
                teacher = get_object_or_404(Teacher, id=teacher_id)
                Course.objects.create(
                    course_code=course_code,
                    course_name=course_name,
                    assigned_teacher=teacher
                )
                messages.success(request, 'Course created successfully.')
                return redirect('admin_courses')

        elif 'delete_course' in request.POST:
            course_id = request.POST['course_id']
            course = get_object_or_404(Course, id=course_id)
            course.delete()
            messages.success(request, 'Course deleted successfully.')
            return redirect('admin_courses')

    courses = Course.objects.all().select_related('assigned_teacher__user')
    teachers = Teacher.objects.all().select_related('user')
    context = {'courses': courses, 'teachers': teachers}
    return render(request, 'academic/admin_courses.html', context)

def admin_announcements(request):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('admin_login')

    if request.method == 'POST':
        if 'create_announcement' in request.POST:
            message = request.POST['message']
            # Create announcement from admin (we'll use the first teacher or create a system announcement)
            try:
                teacher = Teacher.objects.first()
                if teacher:
                    Announcement.objects.create(teacher=teacher, message=message)
                    messages.success(request, 'Announcement created successfully.')
                else:
                    messages.error(request, 'No teachers available to create announcement.')
            except:
                messages.error(request, 'Error creating announcement.')
            return redirect('admin_announcements')

        elif 'delete_announcement' in request.POST:
            announcement_id = request.POST['announcement_id']
            announcement = get_object_or_404(Announcement, id=announcement_id)
            announcement.delete()
            messages.success(request, 'Announcement deleted successfully.')
            return redirect('admin_announcements')

    announcements = Announcement.objects.all().select_related('teacher__user').order_by('-date')
    context = {'announcements': announcements}
    return render(request, 'academic/admin_announcements.html', context)

def admin_reports(request):
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return redirect('admin_login')

    # Generate system reports
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()

    # Course enrollment stats
    course_stats = []
    for course in Course.objects.all():
        student_count = Attendance.objects.filter(course=course).values('student').distinct().count()
        course_stats.append({
            'course': course,
            'students': student_count,
            'assignments': Assignment.objects.filter(course=course).count(),
            'submissions': Submission.objects.filter(assignment__course=course).count()
        })

    # Monthly activity (simplified)
    monthly_stats = {
        'students_registered': Student.objects.filter(user__date_joined__month=11, user__date_joined__year=2025).count(),
        'announcements': Announcement.objects.filter(date__month=11, date__year=2025).count(),
        'assignments': Assignment.objects.filter(created_at__month=11, created_at__year=2025).count(),
    }

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'course_stats': course_stats,
        'monthly_stats': monthly_stats,
    }
    return render(request, 'academic/admin_reports.html', context)
