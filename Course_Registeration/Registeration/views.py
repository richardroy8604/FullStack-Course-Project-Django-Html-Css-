from django.shortcuts import render
from .models import Student, Course, Enrollment
# Create your views here.
def home(request):
    return render(request, 'home.html')

def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html',{'courses': courses})