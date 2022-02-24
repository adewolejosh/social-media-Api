from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserRelationship(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=False)
    follow = models.ForeignKey(User, related_name='followers', default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
