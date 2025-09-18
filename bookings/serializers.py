from rest_framework import serializers
from .models import RoomBooking


class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = [
            'id', 'full_name', 'email', 'phone', 'special_requests',
            'check_in', 'check_out', 'adults', 'children', 
            'selected_rooms', 'total_price', 'nights',
            'booking_date', 'booking_reference'
        ]
        read_only_fields = ['id', 'booking_date', 'booking_reference']
    
    def validate(self, data):
        """Validate booking data"""
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        
        if check_in and check_out:
            if check_out <= check_in:
                raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        selected_rooms = data.get('selected_rooms', {})
        if not selected_rooms:
            raise serializers.ValidationError("At least one room must be selected.")
        
        return data
