from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "profile_picture",
            "bio",
            "followers",
            "following"
        )
        read_only_fields = ("id", "followers", "following")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5, "required": False}}

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)

        return instance


class UserRetrieveSerializer(UserSerializer):
    followers = serializers.StringRelatedField(many=True)
    following = serializers.StringRelatedField(many=True)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        read_only = ("id",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        user.username = user.email[:user.email.index("@")]
        user.save()
        return user
