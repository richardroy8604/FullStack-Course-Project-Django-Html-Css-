from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_dashboard, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Flight URLs
    path('flights/', views.flight_list, name='flight_list'),
    path('flights/add/', views.flight_create, name='flight_create'),
    path('flights/<int:pk>/edit/', views.flight_update, name='flight_update'),
    path('flights/<int:pk>/delete/', views.flight_delete, name='flight_delete'),
    
    # Passenger URLs
    path('passengers/', views.passenger_list, name='passenger_list'),
    path('passengers/add/', views.passenger_create, name='passenger_create'),
    path('passengers/<int:pk>/edit/', views.passenger_update, name='passenger_update'),
    path('passengers/<int:pk>/delete/', views.passenger_delete, name='passenger_delete'),
    
    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/book/', views.book_flight, name='book_flight'),
    path('bookings/book/<int:flight_id>/', views.book_flight, name='book_flight_select'),
    path('bookings/<int:pk>/cancel/', views.booking_delete, name='booking_delete'),
]
