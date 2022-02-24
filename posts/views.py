from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from .models import Post


class PostsView(APIView):
    permissions = [IsAuthenticated]

    def get(self):
        return Post.Objects.all()
