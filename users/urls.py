from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from users.views import (
    CreateUserView,
    RetrieveUpdateUserView,
    follow_user_view,
    unfollow_user_view
)

from django.urls import path

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", RetrieveUpdateUserView.as_view(), name="manage"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("follow/<int:pk>/", follow_user_view, name="follow"),
    path("unfollow/<int:pk>/", unfollow_user_view, name="unfollow"),
]

app_name = "users"
