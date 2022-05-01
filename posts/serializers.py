
from django.utils.timezone import now
from rest_framework import serializers

from .models import Post, PostComment


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        fields = '__all__'


# WORKS
class ReadPostsSerializer(serializers.ModelSerializer):
    post_comments = PostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'desc', 'created_at', 'post_comments']


# WORKS
class CreatePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'desc', 'id', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Post.objects.create(owner=user, **validated_data)
        instance.save()
        return instance


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        fields = ['comment']

    def create(self, validated_data):
        owner = self.context['request'].user
        post = self.context['post']
        instance = PostComment.objects.create(owner=owner, posts=post, **validated_data)
        instance.save()
        return instance
