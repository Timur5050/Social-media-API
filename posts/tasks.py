from celery import shared_task
from posts.models import Post


@shared_task
def create_scheduled_post(post_data, author_id):
    from django.contrib.auth import get_user_model
    author = get_user_model().objects.get(id=author_id)
    Post.objects.create(**post_data, author=author)
