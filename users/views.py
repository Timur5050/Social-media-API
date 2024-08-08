from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from users.serializers import UserCreateSerializer, UserSerializer, UserRetrieveSerializer

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = ()


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
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
    user_to_follow = get_user_model().objects.filter(pk=pk)
    if len(user_to_follow) == 0:
        return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
    user_to_follow = user_to_follow[0]
    if not (user_to_follow.followers.filter(id=request.user.id).exists()):
        user_to_follow.followers.add(request.user)
        return Response("User has been followed successfully", status=status.HTTP_200_OK)

    return Response("You are already following this user", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def unfollow_user_view(request: Request, pk: int) -> Response:
    user_to_unfollow = get_user_model().objects.get(pk=pk)
    if len(user_to_unfollow) == 0:
        return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
    user_to_unfollow = user_to_unfollow[0]
    if request.user.following.filter(id=user_to_unfollow.id).exists():
        user_to_unfollow.followers.remove(request.user)
        return Response("User has been unfollowed successfully", status=status.HTTP_200_OK)

    return Response("You are not following this user", status=status.HTTP_400_BAD_REQUEST)
