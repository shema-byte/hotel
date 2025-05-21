from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'room_type', 'check_in', 'check_out', 'created_at')
    search_fields = ('full_name', 'email', 'mobile_number', 'room_type')
    list_filter = ('room_type', 'guest_type', 'gender', 'check_in', 'check_out')
    ordering = ('-created_at',)