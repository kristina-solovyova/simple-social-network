from django.urls import path
from .views import ProfileAPIView, ProfileFollow, ProfileUnfollow


urlpatterns = [
    path('profile/<int:pk>/follow', ProfileFollow.as_view(), name='follow-profile'),
    path('profile/<int:pk>/unfollow', ProfileUnfollow.as_view(), name='unfollow-profile'),
    path('profile/<int:pk>', ProfileAPIView.as_view(), name='profile-detail'),
]
