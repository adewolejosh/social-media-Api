from django.utils.timezone import now
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
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'desc', 'id', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Post.objects.create(owner=user, **validated_data)
        instance.save()
        return instance


class GetPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

    def get_post(self, **data):
        pass


class GetDeletePostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def destroy(self, post_id):
        instance = Post.objects.filter(id=post_id)
        instance.delete()
        return None
