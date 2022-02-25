from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserRelationship
# from posts.models import Post


class FollowUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')

    class Meta:
        model = UserRelationship
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']
