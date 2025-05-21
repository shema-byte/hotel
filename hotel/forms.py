from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
import re

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name.replace(" ", "").isalpha():
            raise ValidationError("Full name must contain only alphabets.")
        return full_name

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit() or len(mobile) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits.")
        return mobile

    def clean_room_number(self):
        room_number = self.cleaned_data.get('room_number')

        if room_number is None or not str(room_number).isdigit():
            raise ValidationError("Room number must contain only digits.")

        room_number = int(room_number)

        if room_number < 1 or room_number > 20:
            raise ValidationError("Room number must be between 1 and 20.")

        return room_number

    def clean_number_of_people(self):
        num_people = self.cleaned_data.get('number_of_people')
        if num_people is None or num_people < 1 or num_people > 10:
            raise ValidationError("Number of people must be between 1 and 10.")
        return num_people

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@gmail\.com$', email):
            raise ValidationError("Email must be a valid Gmail address ending with '@gmail.com'.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        today = datetime.date.today()

        if check_in and check_in < today:
            self.add_error('check_in', "Check-in date cannot be in the past.")

        if check_out and check_out < today:
            self.add_error('check_out', "Check-out date cannot be in the past.")

        if check_in and check_out and check_out < check_in:
            self.add_error('check_out', "Check-out date cannot be before check-in date.")
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
