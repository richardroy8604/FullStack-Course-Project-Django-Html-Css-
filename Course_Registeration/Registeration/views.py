from django.shortcuts import render
from .models import Student, Course, Enrollment
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')

def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

def register(request):
    if request.method == 'POST':
        student_id= request.POST.get('student')
        course_id = request.POST.get('course_id')
        
        if student_id and course_id:
            # Prevent duplicate entries
            existing_enrollment = Enrollment.objects.filter(student_id=student_id, course_id=course_id).first()
            
            if existing_enrollment:
                messages.warning(request, "You are already enrolled in this course!")
            else:
                student = Student.objects.get(id=student_id)
                course = Course.objects.get(id=course_id)
                Enrollment.objects.create(student=student, course=course)
                messages.success(request, "Successfully enrolled in the course!")
        
        else:
            messages.error(request, "Invalid student or course ID")
        
    stud= Student.objects.all()
    cours= Course.objects.all()
    enr= Enrollment.objects.all()
    context ={
        'stud': stud,
        'cours': cours,
        'enr': enr
    }

    return render(request, 'register.html', context)
