from celery import shared_task
from django.utils import timezone
from .models import Post


@shared_task
def create_scheduled_post(post_data, author_id):
    from django.contrib.auth import get_user_model
    author = get_user_model().objects.get(id=author_id)
    return Post.objects.create(**post_data, author=author)
