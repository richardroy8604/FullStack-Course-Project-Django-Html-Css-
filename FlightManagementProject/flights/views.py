from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Flight, Passenger, Booking
from .forms import FlightForm, PassengerForm, BookingForm, UserRegistrationForm

# Authentication Views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Create associated Passenger profile
            Passenger.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                passport_number=form.cleaned_data['passport_number']
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard and Search View
@login_required
def home_dashboard(request):
    total_flights = Flight.objects.count()
    total_passengers = Passenger.objects.count()
    total_bookings = Booking.objects.count()

    # Flight Search
    source_query = request.GET.get('source', '')
    dest_query = request.GET.get('destination', '')
    date_query = request.GET.get('departure_date', '')

    flights = Flight.objects.all()
    if source_query:
        flights = flights.filter(source__icontains=source_query)
    if dest_query:
        flights = flights.filter(destination__icontains=dest_query)
    if date_query:
        flights = flights.filter(departure_date=date_query)

    context = {
        'total_flights': total_flights,
        'total_passengers': total_passengers,
        'total_bookings': total_bookings,
        'flights': flights,
        'source_query': source_query,
        'dest_query': dest_query,
        'date_query': date_query,
    }
    return render(request, 'home.html', context)

# Flight Management (CRUD)
@login_required
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flights/flight_list.html', {'flights': flights})

@login_required
def flight_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin permissions required.')
        return redirect('flight_list')
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Flight added successfully!')
            return redirect('flight_list')
    else:
        form = FlightForm()
    return render(request, 'flights/flight_form.html', {'form': form, 'title': 'Add Flight'})

@login_required
def flight_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin permissions required.')
        return redirect('flight_list')
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Flight details updated successfully!')
            return redirect('flight_list')
    else:
        form = FlightForm(instance=flight)
    return render(request, 'flights/flight_form.html', {'form': form, 'title': 'Edit Flight'})

@login_required
def flight_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin permissions required.')
        return redirect('flight_list')
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        flight.delete()
        messages.success(request, 'Flight deleted successfully!')
        return redirect('flight_list')
    return render(request, 'flights/flight_confirm_delete.html', {'flight': flight})

# Passenger Management (CRUD)
@login_required
def passenger_list(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin permissions required.')
        return redirect('home')
    passengers = Passenger.objects.all()
    return render(request, 'passengers/passenger_list.html', {'passengers': passengers})

@login_required
def passenger_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin permissions required.')
        return redirect('passenger_list')
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Passenger added successfully!')
            return redirect('passenger_list')
    else:
        form = PassengerForm()
    return render(request, 'passengers/passenger_form.html', {'form': form, 'title': 'Add Passenger'})

@login_required
def passenger_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin permissions required.')
        return redirect('passenger_list')
    passenger = get_object_or_404(Passenger, pk=pk)
    if request.method == 'POST':
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            messages.success(request, 'Passenger details updated successfully!')
            return redirect('passenger_list')
    else:
        form = PassengerForm(instance=passenger)
    return render(request, 'passengers/passenger_form.html', {'form': form, 'title': 'Edit Passenger'})

@login_required
def passenger_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin permissions required.')
        return redirect('passenger_list')
    passenger = get_object_or_404(Passenger, pk=pk)
    if request.method == 'POST':
        passenger.delete()
        messages.success(request, 'Passenger deleted successfully!')
        return redirect('passenger_list')
    return render(request, 'passengers/passenger_confirm_delete.html', {'passenger': passenger})

# Flight Booking Module
@login_required
def book_flight(request, flight_id=None):
    selected_flight = get_object_or_404(Flight, pk=flight_id) if flight_id else None

    # Get passenger profile if logged in as regular passenger
    passenger_profile = getattr(request.user, 'passenger_profile', None)

    if request.method == 'POST':
        flight_pk = request.POST.get('flight') or flight_id
        passenger_pk = request.POST.get('passenger')

        if not passenger_pk and passenger_profile:
            passenger_pk = passenger_profile.pk

        if not flight_pk or not passenger_pk:
            messages.error(request, 'Please select both a passenger and a flight.')
            return redirect('book_flight', flight_id=flight_id) if flight_id else redirect('book_flight')

        flight = get_object_or_404(Flight, pk=flight_pk)
        passenger = get_object_or_404(Passenger, pk=passenger_pk)

        # Check duplicate booking requirement
        if Booking.objects.filter(passenger=passenger, flight=flight).exists():
            messages.error(request, f'Duplicate Booking! {passenger} has already booked Flight {flight.flight_number}.')
        else:
            Booking.objects.create(passenger=passenger, flight=flight)
            messages.success(request, f'Booking confirmed for {passenger} on Flight {flight.flight_number}!')
            return redirect('booking_list')

    flights = Flight.objects.all()
    passengers = Passenger.objects.all()
    return render(request, 'bookings/book_flight.html', {
        'flights': flights,
        'passengers': passengers,
        'selected_flight': selected_flight,
        'passenger_profile': passenger_profile
    })

@login_required
def booking_list(request):
    if request.user.is_staff:
        bookings = Booking.objects.all().select_related('passenger', 'flight')
    else:
        passenger_profile = getattr(request.user, 'passenger_profile', None)
        bookings = Booking.objects.filter(passenger=passenger_profile).select_related('passenger', 'flight') if passenger_profile else []

    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # Check permissions
    if not request.user.is_staff and getattr(request.user, 'passenger_profile', None) != booking.passenger:
        messages.error(request, 'Unauthorized action.')
        return redirect('booking_list')

    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('booking_list')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})
