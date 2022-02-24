from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import *


# Create your views here.
class UserProfile(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)


class FollowUser(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, user_id):
        print("this is the user id", user_id)
        print(request.user.pk)
        follow = {'me': request.user.pk, 'follow': user_id}
        serializer = FollowUserSerializer(data=follow)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class UnFollowUser(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, user_id):
        search = User.objects.filter(pk=user_id)
        user = request.user
        serializer = UnFollowUserSerializer(search)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)
