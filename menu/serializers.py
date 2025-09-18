# _file: dining_project/menu/serializers.py_
from rest_framework import serializers
from .models import MenuItem, DailySpecial

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image']

class DailySpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySpecial
        fields = ['id', 'name', 'description', 'price', 'image', 'date', 'is_active', 'created_at', 'updated_at']