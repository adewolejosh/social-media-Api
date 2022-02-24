from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)


class PostComment(models.Model):
    owner = models.ForeignKey(User, related_name='comment_owner', on_delete=models.CASCADE)
    posts = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
