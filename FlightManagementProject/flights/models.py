from django.db import models
from django.contrib.auth.models import User

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='passenger_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    capacity = models.IntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number} ({self.source} to {self.destination})"

class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Confirmed')

    class Meta:
        unique_together = ('passenger', 'flight')

    def __str__(self):
        return f"{self.passenger} - {self.flight.flight_number}"
