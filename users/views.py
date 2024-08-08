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

