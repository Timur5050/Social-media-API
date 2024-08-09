from django.db.models import F, Q
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from posts.models import Post, Comment, Like
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer, PostRetrieveSerializer, CommentSerializer

from django.shortcuts import render


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "retrieve":
            serializer = PostRetrieveSerializer
        elif self.action == "list":
            serializer = PostSerializer

        return serializer

    def get_queryset(self):
        queryset = self.queryset.filter(Q(author__followers=self.request.user.id) | Q(author__exact=self.request.user))
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset


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


@api_view(["GET", "POST"])
def like_post(request: Request, pk: int) -> Response:
    post = get_object_or_404(Post.objects.all(), pk=pk)
    print(request.user in post.author.followers.all())
    if request.user not in post.author.followers.all():
        return Response("You need to follow the author of post to like it", status=status.HTTP_400_BAD_REQUEST)
    if request.user.id in [i["author"] for i in list(post.likes.values("author"))]:
        return Response("You have already liked this post", status=status.HTTP_400_BAD_REQUEST)
    Like.objects.create(author=request.user, post=post)
    serializer = PostRetrieveSerializer(post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def unlike_post(request: Request, pk: int) -> Response:
    post = get_object_or_404(Post.objects.all(), pk=pk)
    if request.user not in post.author.followers.all():
        return Response("You need to follow the author of post to unlike it", status=status.HTTP_400_BAD_REQUEST)
    if request.user.id not in [i["author"] for i in list(post.likes.values("author"))]:
        return Response("You have not liked this post", status=status.HTTP_400_BAD_REQUEST)
    like_to_delete = Like.objects.get(author=request.user, post=post)
    like_to_delete.delete()
    serializer = PostRetrieveSerializer(post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_liked_posts(request: Request) -> Response:
    posts = Post.objects.filter(likes__author__exact=request.user.id)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
