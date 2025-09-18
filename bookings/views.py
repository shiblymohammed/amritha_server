from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import RoomBooking
from .serializers import RoomBookingSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def room_bookings_view(request):
    """
    Handle both GET (list bookings) and POST (create booking) requests
    """
    if request.method == 'GET':
        # Handle listing bookings with optional filters
        try:
            bookings = RoomBooking.objects.all()
            
            # Apply filters
            limit = request.GET.get('limit')
            ordering = request.GET.get('ordering', '-booking_date')
            search = request.GET.get('search')
            
            if search:
                bookings = bookings.filter(
                    full_name__icontains=search
                ) | bookings.filter(
                    email__icontains=search
                ) | bookings.filter(
                    booking_reference__icontains=search
                )
            
            # Apply ordering
            if ordering:
                bookings = bookings.order_by(ordering)
            
            # Apply limit
            if limit:
                try:
                    limit = int(limit)
                    bookings = bookings[:limit]
                except ValueError:
                    pass
            
            serializer = RoomBookingSerializer(bookings, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching bookings: {str(e)}")
            return Response({
                'success': False,
                'message': 'Failed to fetch bookings',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        # Handle creating a new booking
        serializer = RoomBookingSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Save the booking
                booking = serializer.save()
                logger.info(f"New booking created: {booking.booking_reference}")
                
                # Send email notification to admin
                try:
                    send_booking_confirmation_email(booking)
                    logger.info(f"Email sent for booking: {booking.booking_reference}")
                except Exception as e:
                    logger.error(f"Failed to send email for booking {booking.booking_reference}: {str(e)}")
                    # Don't fail the booking if email fails
                
                return Response({
                    'success': True,
                    'message': 'Booking created successfully!',
                    'booking_reference': booking.booking_reference,
                    'data': RoomBookingSerializer(booking).data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Error creating booking: {str(e)}")
                return Response({
                    'success': False,
                    'message': 'Failed to create booking. Please try again.',
                    'errors': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'success': False,
            'message': 'Invalid booking data.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_room_booking(request, booking_reference):
    """
    Get a specific booking by reference
    """
    try:
        booking = RoomBooking.objects.get(booking_reference=booking_reference)
        serializer = RoomBookingSerializer(booking)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except RoomBooking.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Booking not found.'
        }, status=status.HTTP_404_NOT_FOUND)


def send_booking_confirmation_email(booking):
    """
    Send booking confirmation email to admin
    """
    try:
        # Prepare email context
        context = {
            'booking': booking,
        }
        
        # Render HTML email
        html_message = render_to_string('bookings/booking_confirmation_email.html', context)
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # Email subject
        subject = f'🏛️ New Heritage Hotel Booking - {booking.booking_reference}'
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        logger.error(f"Failed to send booking confirmation email: {str(e)}")
        raise e


@api_view(['GET'])
@permission_classes([AllowAny])
def get_booking_stats(request):
    """
    Get booking statistics for the dashboard
    """
    try:
        # Get all bookings
        all_bookings = RoomBooking.objects.all()
        
        # Count bookings by status
        pending_count = all_bookings.filter(status='pending').count()
        confirmed_count = all_bookings.filter(status='confirmed').count()
        cancelled_count = all_bookings.filter(status='cancelled').count()
        completed_count = all_bookings.filter(status='completed').count()
        
        # Calculate total revenue
        total_revenue = all_bookings.aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        # Calculate monthly revenue (current month)
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_revenue = all_bookings.filter(
            booking_date__gte=current_month
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        # Calculate average booking value
        avg_booking_value = all_bookings.aggregate(
            avg=Avg('total_price')
        )['avg'] or 0
        
        # Calculate total guests
        total_guests = all_bookings.aggregate(
            total_adults=Sum('adults'),
            total_children=Sum('children')
        )
        total_guests = (total_guests['total_adults'] or 0) + (total_guests['total_children'] or 0)
        
        # Recent bookings count (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        recent_bookings_count = all_bookings.filter(booking_date__gte=week_ago).count()
        
        # Calculate occupancy rate (simplified - assuming 100 total rooms)
        total_rooms = 100
        occupied_rooms = confirmed_count + completed_count
        occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0
        
        stats = {
            'total_bookings': all_bookings.count(),
            'pending_bookings': pending_count,
            'confirmed_bookings': confirmed_count,
            'cancelled_bookings': cancelled_count,
            'completed_bookings': completed_count,
            'total_revenue': str(total_revenue),
            'monthly_revenue': str(monthly_revenue),
            'average_booking_value': str(round(avg_booking_value, 2)),
            'occupancy_rate': round(occupancy_rate, 1),
            'total_guests': total_guests,
            'recent_bookings_count': recent_bookings_count
        }
        
        return Response({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        logger.error(f"Error fetching booking stats: {str(e)}")
        return Response({
            'success': False,
            'message': 'Failed to fetch statistics'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_booking_status(request, booking_id):
    """
    Update booking status
    """
    try:
        booking = RoomBooking.objects.get(id=booking_id)
        new_status = request.data.get('status')
        
        if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
            booking.status = new_status
            booking.save()
            
            return Response({
                'success': True,
                'message': 'Booking status updated successfully',
                'data': RoomBookingSerializer(booking).data
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid status'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except RoomBooking.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error updating booking status: {str(e)}")
        return Response({
            'success': False,
            'message': 'Failed to update booking status'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_booking(request, booking_id):
    """
    Delete a booking
    """
    try:
        booking = RoomBooking.objects.get(id=booking_id)
        booking.delete()
        
        return Response({
            'success': True,
            'message': 'Booking deleted successfully'
        })
        
    except RoomBooking.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error deleting booking: {str(e)}")
        return Response({
            'success': False,
            'message': 'Failed to delete booking'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_recent_bookings(request):
    """
    Get recent bookings for notifications
    """
    try:
        # Get bookings from last 24 hours
        yesterday = timezone.now() - timedelta(days=1)
        recent_bookings = RoomBooking.objects.filter(
            created_at__gte=yesterday
        ).order_by('-created_at')[:10]
        
        notifications = []
        for booking in recent_bookings:
            notifications.append({
                'id': booking.id,
                'type': 'new_booking',
                'title': f'New Booking: {booking.booking_reference}',
                'message': f'{booking.guest_name} booked {booking.room_type} for {booking.check_in_date}',
                'timestamp': booking.created_at.isoformat(),
                'read': False,
                'booking_id': booking.id
            })
        
        return Response({
            'success': True,
            'data': notifications
        })
        
    except Exception as e:
        logger.error(f"Error fetching recent bookings: {str(e)}")
        return Response({
            'success': False,
            'message': 'Failed to fetch recent bookings'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
