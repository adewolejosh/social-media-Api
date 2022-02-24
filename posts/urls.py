
from django.urls import path
from .views import PostsView

urlpatterns = [
    path('authenticate/', PostsView.as_view())
]