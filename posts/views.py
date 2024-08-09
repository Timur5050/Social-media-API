from django.db.models import Q
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Like, Comment
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer, PostRetrieveSerializer, CommentSerializer


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
        queryset = self.queryset.filter(
            Q(author__followers=self.request.user.id)
            | Q(author__exact=self.request.user)
        ).select_related("author").prefetch_related("comments").prefetch_related("likes")
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return_queryset = PostSerializer(self.get_queryset(), many=True)
        return Response(return_queryset.data, status=status.HTTP_201_CREATED)


class MyPostsViewSet(PostViewSet):
    def get_queryset(self):
        queryset = (self.queryset.filter(author=self.request.user)
                    .select_related("author").prefetch_related("comments")
                    .prefetch_related("likes"))
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


class ManageCommentView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, ]


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
