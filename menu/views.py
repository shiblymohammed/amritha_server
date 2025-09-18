# _file: dining_project/menu/views.py_
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import MenuItem, DailySpecial
from .serializers import MenuItemSerializer, DailySpecialSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().order_by('name')
    serializer_class = MenuItemSerializer

class DailySpecialViewSet(viewsets.ModelViewSet):
    queryset = DailySpecial.objects.all().order_by('-created_at')
    serializer_class = DailySpecialSerializer

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        daily_special = self.get_object()
        daily_special.is_active = True
        daily_special.save()
        return Response({'status': 'daily special activated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        daily_special = self.get_object()
        daily_special.is_active = False
        daily_special.save()
        return Response({'status': 'daily special deactivated'}, status=status.HTTP_200_OK)

class ActiveDailySpecialsListView(ListAPIView):
    serializer_class = DailySpecialSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return DailySpecial.objects.filter(date=today, is_active=True)