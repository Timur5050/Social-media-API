import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


def image_path(instance, filename):
    _, extension = os.path.splitext(filename)
    url = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/post-images/", url)


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(null=True, upload_to=image_path)
    creation_time = models.DateTimeField(null=True, blank=True)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )


class Like(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="likes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
