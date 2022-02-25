from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserRelationship(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow = models.ManyToManyField(User, related_name='followers', symmetrical=False)

    def __str__(self):
        return f'{self.user}'
