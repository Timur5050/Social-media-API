from django.urls import path, include

from rest_framework import routers

from posts.views import (
    PostViewSet,
    MyPostsViewSet,
    ManageCommentView,
    create_comment,
    like_post,
    unlike_post,
    get_liked_posts
)

router1 = routers.DefaultRouter()
router2 = routers.DefaultRouter()

router1.register("posts", PostViewSet)
router2.register("my", MyPostsViewSet)

urlpatterns = [
    path("", include(router1.urls)),
    path("", include(router2.urls)),
    path("comment/<int:pk>/", create_comment, name="comment_post"),
    path("comment/manage/<int:pk>/", ManageCommentView.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    }), name="manage_comment"),
    path("like/<int:pk>/", like_post, name="like_post"),
    path("unlike/<int:pk>/", unlike_post, name="unlike_post"),
    path("liked/", get_liked_posts, name="liked-posts")
]

app_name = "posts"
