from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, PostComment
from accounts.serializers import UserSerializer


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'


class ReadPostsSerializer(serializers.ModelSerializer):
    comments = PostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'desc', 'created_at', 'comments']


class CreatePostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        instance = Post.objects.create(**validated_data)
        instance.save()
        return instance


class GetDeletePostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def destroy(self, post_id):
        instance = Post.objects.filter(id=post_id)
        instance.delete()
        return None
