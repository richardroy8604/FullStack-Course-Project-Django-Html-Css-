from django import forms
from django.contrib.auth.models import User
from .models import Flight, Passenger, Booking

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'source', 'destination', 'departure_date', 'departure_time', 'capacity', 'price']
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'email', 'phone', 'passport_number']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger', 'flight']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20)
    passport_number = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
