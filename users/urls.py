from users.views import CreateUserView, RetrieveUpdateUserView

from django.urls import path

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", RetrieveUpdateUserView.as_view(), name="manage"),
]

app_name = "users"
