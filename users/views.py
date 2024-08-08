from users.serializers import UserCreateSerializer, UserSerializer

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = ()


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    # permission_classes = ()

    def get_object(self):
        return self.request.user
