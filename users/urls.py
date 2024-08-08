from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

from users.views import CreateUserView, RetrieveUpdateUserView

from django.urls import path

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", RetrieveUpdateUserView.as_view(), name="manage"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "users"
