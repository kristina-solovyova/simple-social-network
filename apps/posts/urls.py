from django.urls import path
from .views import (
    PostAPIView, PostLike, PostUnlike, PostDetailAPIView
)


urlpatterns = [
    path('posts/<int:pk>/like', PostLike.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike', PostUnlike.as_view(), name='unlike-post'),
    path('posts/<int:pk>', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts', PostAPIView.as_view(), name='post-list'),
]
