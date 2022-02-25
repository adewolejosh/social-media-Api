import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from .serializers import *


# Create your views here.
from .models import Post


class ReadAllPostsView(APIView):
    permissions = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        post = Post.objects.filter(owner=user)
        serializer = ReadPostsSerializer(post, many=True)
        return Response(serializer.data, HTTP_200_OK)


class GetDeletePostView(APIView):
    permissions = (IsAuthenticated,)

    def get(self, request, post_id):
        user = request.user
        post = Post.objects.filter(owner=user, id=post_id)
        return Response({"message": json.load(post)}, status=HTTP_200_OK)

    def delete(self, request, post_id):
        user = request.user
        post = Post.objects.filter(owner=user, id=post_id)
        serializer = GetDeletePostSerializer(post)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, HTTP_200_OK)


class CreatePostView(APIView):
    permissions = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = CreatePostSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        except User.DoesNotExist:
            return
