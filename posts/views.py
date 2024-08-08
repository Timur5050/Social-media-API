from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from posts.models import Post, Comment
from posts.serializers import PostSerializer, PostRetrieveSerializer, CommentSerializer

from django.shortcuts import render


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "retrieve":
            serializer = PostRetrieveSerializer
        elif self.action == "list":
            serializer = PostSerializer

        return serializer


class MyPostsViewSet(PostViewSet):
    def get_queryset(self):
        queryset = self.queryset.filter(author=self.request.user)
        return queryset


@api_view(["GET", "POST"])
def create_comment(request: Request, pk: int) -> Response:
    if request.method == 'GET':
        return Response({
            "text": "Enter comment text here"
        })

    post = get_object_or_404(Post.objects.all(), pk=pk)
    request.data["post"] = post.id
    request.data["author"] = request.user.id
    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
