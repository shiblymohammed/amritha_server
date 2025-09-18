# _file: dining_project/menu/admin.py_
from django.contrib import admin
from .models import MenuItem, DailySpecial

admin.site.register(MenuItem)
admin.site.register(DailySpecial)