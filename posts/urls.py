
from django.urls import path
from .views import *

urlpatterns = [
    path('all_posts/', ReadAllPostsView.as_view()),
    path('', CreatePostView.as_view()),
    path('<int:id>', GetDeletePostView.as_view()),
]
