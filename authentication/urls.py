from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    LogoutView,
    UserProfileView,
    ChangePasswordView,
    check_auth_status,
    CreateAdminUserView,
    CustomTokenObtainPairView
)

urlpatterns = [
    # Authentication endpoints
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User management endpoints
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('status/', check_auth_status, name='auth_status'),
    
    # Admin user management (superuser only)
    path('create-admin/', CreateAdminUserView.as_view(), name='create_admin_user'),
]