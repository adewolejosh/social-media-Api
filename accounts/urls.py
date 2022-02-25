
from django.urls import path
from .views import UserProfile, FollowUser, UnFollowUser

urlpatterns = [
    path('user/', UserProfile.as_view()),
    path('follow/<int:user_id>/', FollowUser.as_view()),
    path('unfollow/<int:user_id>/', UnFollowUser.as_view()),
]
