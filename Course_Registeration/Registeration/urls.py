from django.urls import path
from Registeration import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('register/', views.register, name='register'),
]