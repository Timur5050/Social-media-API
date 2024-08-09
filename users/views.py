from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from users.serializers import UserCreateSerializer, UserSerializer, UserRetrieveSerializer

from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404, \
    RetrieveUpdateDestroyAPIView


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = ()


class RetrieveUpdateUserView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    # permission_classes = ()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.request.method == "GET":
            serializer = UserRetrieveSerializer
        elif self.request.method == "POST":
            serializer = UserRetrieveSerializer

        return serializer


@api_view(["GET", "POST"])
def follow_user_view(request: Request, pk: int) -> Response:
    user_to_follow = get_object_or_404(get_user_model().objects.all(), pk=pk)
    if not (user_to_follow.followers.filter(id=request.user.id).exists()):
        if user_to_follow.id == request.user.id:
            return Response("You can not follow yourself", status=status.HTTP_400_BAD_REQUEST)
        user_to_follow.followers.add(request.user)
        return Response("User has been followed successfully", status=status.HTTP_200_OK)

    return Response("You are already following this user", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def unfollow_user_view(request: Request, pk: int) -> Response:
    user_to_unfollow = get_object_or_404(get_user_model().objects.all(), pk=pk)
    if request.user.following.filter(id=user_to_unfollow.id).exists():
        if user_to_unfollow.id == request.user.id:
            return Response("You can not unfollow yourself", status=status.HTTP_400_BAD_REQUEST)
        user_to_unfollow.followers.remove(request.user)
        return Response("User has been unfollowed successfully", status=status.HTTP_200_OK)

    return Response("You are not following this user", status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveListAPIView(
    ListModelMixin,
    RetrieveModelMixin,
    GenericAPIView
):
    queryset = get_user_model().objects.all()
    serializer_class = UserRetrieveSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        if "pk" in kwargs:
            if kwargs["pk"] == request.user.id:
                return redirect(reverse("users:manage"))
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        username = self.request.query_params.get("username", None)
        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset
