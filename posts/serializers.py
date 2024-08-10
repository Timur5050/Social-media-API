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
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ("author", "created", "text")


class PostSerializer(serializers.ModelSerializer):
    count_of_comments = serializers.IntegerField(source="comments.count", read_only=True)
    count_of_likes = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "description",
            "created",
            "count_of_comments",
            "count_of_likes",
            "creation_time"
        )

    def create(self, validated_data):
        return Post.objects.create(
            **validated_data,
            author=self.context["request"].user
        )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PostRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)
    likes = serializers.SlugRelatedField(slug_field="author.username", read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "description",
            "author",
            "created",
            "comments",
            "likes",
            "post_image"
        )
