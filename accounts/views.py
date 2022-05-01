
from django.db.models import Count, Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import *


# Create your views here.
class UserProfile(APIView):
    permissions = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        ff = UserRelationship.objects.filter(user=user).annotate(ff_count=Count('follow')).aggregate(total_ff=Sum('ff_count'))
        followers = UserRelationship.objects.filter(follow=request.user).count()
        data = {'user': serializer.data, 'followers': followers, 'following': ff['total_ff']}
        return Response(data, status=HTTP_200_OK)


class FollowUser(APIView):
    permissions = (IsAuthenticated,)

    def post(self, request, user_id):
        try:
            if not request.user:
                raise User.DoesNotExist
            if request.user.id == user_id:
                raise User.DoesNotExist
            follow = User.objects.get(id=user_id)
            if user_id and request.user:
                if UserRelationship.objects.filter(user=request.user, follow=follow):
                    return Response({"message": "Already Followed!"}, status=HTTP_204_NO_CONTENT)
                elif UserRelationship.objects.filter(user=request.user):
                    rel = UserRelationship.objects.get(user=request.user)
                    rel.follow.add(follow)
                    rel.save()
                else:
                    data = UserRelationship()
                    data.user = request.user
                    data.save()
                    data.follow.add(follow)
                    data.save()

                return Response({"message": "Followed!"}, status=HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "User does not exist or Not cyclic"}, status=HTTP_404_NOT_FOUND)


class UnFollowUser(APIView):

    def post(self, request, user_id):
        try:
            if not request.user:
                raise User.DoesNotExist
            if request.user.id == user_id:
                raise User.DoesNotExist
            follow = User.objects.get(id=user_id)
            if user_id and request.user:
                rel = UserRelationship.objects.get(user=request.user)
                if rel:
                    rel.follow.remove(follow)
                    rel.save()
                    return Response({"message": "UnFollowed!"}, status=HTTP_200_OK)
                return Response({"message": "No Relationship exists!"}, status=HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({"message": "User does not exist or Not cyclic"}, status=HTTP_404_NOT_FOUND)

