from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CreateUserView, register_page, LoginView, CustomTokenObtainPairView, LogoutView

app_name = "user"

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("register/user/", CreateUserView.as_view(), name="create"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
