from posts.models import Post, Comment

from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "author", "created", "text", "post")

    def create(self, validated_data):
        return Comment.objects.create(
            **validated_data
        )


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("author", "created", "text")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "description", "created")

    def create(self, validated_data):
        return Post.objects.create(**validated_data, author=self.context["request"].user)


class PostRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "description", "author", "created", "comments")
