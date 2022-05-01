
from django.urls import path
from .views import *

urlpatterns = [
    path('', CreatePostView.as_view()),
    path('all_posts/', ReadAllPostsView.as_view()),
    path('<int:post_id>/', GetDeletePostView.as_view()),
    path('<int:post_id>/like/', LikePostView.as_view()),
    path('<int:post_id>/unlike/', UnlikePostView.as_view()),
    path('<int:post_id>/comment/', CRDCommentView.as_view()),
]
