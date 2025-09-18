from django.db import models
from django.utils import timezone
import json


class RoomBooking(models.Model):
    # Guest Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    special_requests = models.TextField(blank=True, null=True)
    
    # Booking Details
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    
    # Room and Pricing Information
    selected_rooms = models.JSONField()  # Store room selections as JSON
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    nights = models.PositiveIntegerField()
    
    # Metadata
    booking_date = models.DateTimeField(default=timezone.now)
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)
    
    # Status field
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Room Booking'
        verbose_name_plural = 'Room Bookings'
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate a booking reference
            import random
            import string
            self.booking_reference = 'HH' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_reference} - {self.full_name}"
    
    @property
    def room_details(self):
        """Helper property to get formatted room details"""
        # Room data mapping (same as in frontend)
        rooms_data = {
            1: {"name": "The President's Chamber — Deluxe", "price": 8500},
            2: {"name": "The Magistrate's Chamber — Executive", "price": 10500},
            3: {"name": "The Collector's Chamber — Deluxe", "price": 7500},
            4: {"name": "The Residency Room — Executive", "price": 9500},
            5: {"name": "The Plantation Room — Deluxe", "price": 6500},
        }
        
        selected = self.selected_rooms
        room_list = []
        
        for room_id, quantity in selected.items():
            room_id = int(room_id)
            if room_id in rooms_data:
                room_info = rooms_data[room_id]
                room_list.append({
                    'name': room_info['name'],
                    'quantity': quantity,
                    'price_per_night': room_info['price'],
                    'total_price': room_info['price'] * quantity
                })
        
        return room_list
