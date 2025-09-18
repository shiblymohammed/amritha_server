# _file: dining_project/menu/urls.py_
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, DailySpecialViewSet, ActiveDailySpecialsListView

router = DefaultRouter()
router.register(r'items', MenuItemViewSet)
router.register(r'daily-specials', DailySpecialViewSet)

urlpatterns = [
    path('daily-specials/active/', ActiveDailySpecialsListView.as_view(), name='active-daily-specials-list'),
    path('', include(router.urls)),
]