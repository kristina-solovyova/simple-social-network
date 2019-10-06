from django.urls import path
from .views import PostAPIView, PostLike, PostUnlike


urlpatterns = [
    path('posts/<int:pk>/like', PostLike.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike', PostUnlike.as_view(), name='unlike-post'),
    path('posts', PostAPIView.as_view()),
]
