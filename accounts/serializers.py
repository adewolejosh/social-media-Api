from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserRelationship


class FollowUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserRelationship
        fields = '__all__'

    def create(self, validated_data):
        follow = validated_data['follow']
        new_Relationship = UserRelationship.objects.create(follow=follow)
        new_Relationship.save()
        return new_Relationship


class UnFollowUserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = UserRelationship

    def update(self, instance, validated_data):
        user = validated_data['user']
        unfollow = validated_data['search']
        rel = UserRelationship.objects.filter(id=unfollow).delete()
        user.objects.delete()
        user.save()
        rel.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    follow = FollowUserSerializer(read_only=True, many=True)

    class Meta:
        model = User
        read_only_fields = ['follow']
        exclude = ('password', 'is_superuser', 'is_active', 'is_staff', 'last_login', )



