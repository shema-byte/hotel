from django.db import models

class Booking(models.Model):
    ROOM_CHOICES = [
        ('Standard Room', 'Standard Room'),
        ('Deluxe Room', 'Deluxe Room'),
        ('Family Room', 'Family Room'),
        ('Executive Suite', 'Executive Suite'),
        ('Presidential Suite', 'Presidential Suite'),
        ('Honeymoon Suite', 'Honeymoon Suite'),
    ]
    
    GUEST_TYPE_CHOICES = [
        ('bachelors', 'Bachelors'),
        ('couple', 'Couple'),
        ('family', 'Family'),
    ]
    
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    number_of_people = models.PositiveIntegerField(default=1)
    room_type = models.CharField(max_length=50, choices=ROOM_CHOICES)
    guest_type = models.CharField(max_length=20, choices=GUEST_TYPE_CHOICES)
    check_in = models.DateField()
    check_out = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        """Check if booking is active based on check-in and check-out dates."""
        from datetime import date
        today = date.today()
        return self.check_in <= today <= self.check_out

    def __str__(self):
        return f"{self.full_name} - {self.room_type}"