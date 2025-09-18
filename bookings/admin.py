from django.contrib import admin
from .models import RoomBooking


@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_reference', 'full_name', 'email', 'check_in', 
        'check_out', 'nights', 'total_price', 'booking_date'
    ]
    list_filter = ['check_in', 'check_out', 'booking_date', 'adults']
    search_fields = ['booking_reference', 'full_name', 'email', 'phone']
    readonly_fields = ['booking_reference', 'booking_date']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_reference', 'booking_date')
        }),
        ('Guest Information', {
            'fields': ('full_name', 'email', 'phone', 'special_requests')
        }),
        ('Stay Details', {
            'fields': ('check_in', 'check_out', 'adults', 'children', 'nights')
        }),
        ('Room & Pricing', {
            'fields': ('selected_rooms', 'total_price')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing booking
            return self.readonly_fields + ['selected_rooms', 'total_price']
        return self.readonly_fields
