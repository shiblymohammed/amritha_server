from django.urls import path
from . import views

urlpatterns = [
    path('room-bookings/', views.room_bookings_view, name='room_bookings'),
    path('room-bookings/create/', views.room_bookings_view, name='create_room_booking'),  # Backward compatibility
    path('room-bookings/stats/', views.get_booking_stats, name='get_booking_stats'),
    path('room-bookings/<int:booking_id>/status/', views.update_booking_status, name='update_booking_status'),
    path('room-bookings/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('room-bookings/<str:booking_reference>/', views.get_room_booking, name='get_room_booking'),
    path('recent-bookings/', views.get_recent_bookings, name='get_recent_bookings'),
]
