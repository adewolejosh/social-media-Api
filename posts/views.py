
from django.db.models import Count, Sum

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from .serializers import *
from .models import *


# Create your views here.
class ReadAllPostsView(APIView):
    permissions = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        user = request.user
        post = Post.objects.filter(owner=user)
        serializer = ReadPostsSerializer(post, many=True)
        return Response(serializer.data, HTTP_200_OK)


class GetDeletePostView(APIView):
    permissions = (IsAuthenticatedOrReadOnly,)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            likes = PostLike.objects.filter(liked_post=post).annotate(like_count=Count('liked_by')).aggregate(total_like=Sum('like_count'))
            data = {"post": {"owner": f"{post.owner}", "title": f"{post.title}", "desc": f"{post.desc}", "likes": likes['total_like']}}
            return Response(data, status=HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"message": "No such Post exist"}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        try:
            user = request.user
            post = Post.objects.filter(owner=user, id=post_id).delete()
            return Response({"message": f"deleted! {post}"}, HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"message": "No such Post exist"}, status=HTTP_404_NOT_FOUND)


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


class CRDCommentView(APIView):
    permissions = (IsAuthenticatedOrReadOnly,)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            comments = PostComment.objects.filter(posts=post.pk)
            data = {"comments": f"{comments}"}
            return Response(data, status=HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"message": "Post Not Found"}, status=HTTP_404_NOT_FOUND)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            serializer = CreateCommentSerializer(
                data=request.data, context={'request': request, 'post': post}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "User/Comment Not Found"}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        try:
            user = request.user
            post = PostComment.objects.get(owner=user, posts=post_id).delete()
            return Response({"message": f"deleted! {post}"}, status=HTTP_200_OK)
        except PostComment.DoesNotExist:
            return Response({"message": "Comment Does Not Exist"}, HTTP_404_NOT_FOUND)


class LikePostView(APIView):
    permissions = (IsAuthenticated,)

    def post(self, request, post_id):
        try:
            user = request.user
            post = Post.objects.get(id=post_id)
            if post and user:
                if PostLike.objects.filter(liked_post=post, liked_by=user):
                    return Response({"message": "Already Liked"}, status=HTTP_204_NO_CONTENT)
                elif PostLike.objects.filter(liked_post=post):
                    like = PostLike.objects.get(user=user)
                    like.liked_by.add(user)
                    like.save()
                else:
                    data = PostLike()
                    data.liked_post = post
                    data.save()
                    data.liked_by.add(user)
                    data.save()

                return Response({"message": "liked!"}, status=HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"message": "Post Does Not Exist"}, status=HTTP_404_NOT_FOUND)


class UnlikePostView(APIView):
    permissions = (IsAuthenticated,)

    def post(self, request, post_id):
        try:
            user = request.user
            post = Post.objects.get(id=post_id)
            liked_post = PostLike.objects.get(liked_post=post, liked_by=user)
            if post and liked_post:
                liked_post.liked_by.remove(user)
                return Response({"message": "Unliked"}, status=HTTP_200_OK)
            return Response({"message": "Can't Unlike a not Liked :p"}, status=HTTP_404_NOT_FOUND)
        except PostLike.DoesNotExist:
            return Response({"message": "Post Does Not Exist/ Can't Unlike"}, status=HTTP_404_NOT_FOUND)
