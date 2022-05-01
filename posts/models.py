from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=now())

    def __str__(self):
        return f'{self.owner} - {self.title}'


class PostComment(models.Model):
    owner = models.ForeignKey(User, related_name='comment_owner', on_delete=models.CASCADE)
    posts = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=now())

    def __str__(self):
        return f'{self.owner} - {self.posts} - {self.comment}'


class PostLike(models.Model):
    liked_post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='like_this_post')

    def __str__(self):
        return f'{self.liked_post} has likes'
