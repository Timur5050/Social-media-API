from django.urls import path, include

from rest_framework import routers

from posts.views import (
    PostViewSet,
    MyPostsViewSet,
    create_comment
)

router1 = routers.DefaultRouter()
router2 = routers.DefaultRouter()

router1.register("posts", PostViewSet)
router2.register("my", MyPostsViewSet)

urlpatterns = [
    path("", include(router1.urls)),
    path("", include(router2.urls)),
    path("comment/<int:pk>/", create_comment, name="comment_post"),
]

app_name = "posts"
