from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status
from .serializers import ProfileSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Profile


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user')


class ProfileFollow(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        follower = request.user.profile

        try:
            followee = Profile.objects.get(pk=self.kwargs['pk'])
        except Profile.DoesNotExist:
            raise NotFound('There is no profile with given ID.')

        if follower.pk is followee.pk:
            raise ValidationError('You can not follow yourself.')

        if follower.is_following(followee):
            raise ValidationError('You are already following profile with given ID.')

        follower.follow(followee)
        serializer = self.serializer_class(followee, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUnfollow(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        follower = request.user.profile

        try:
            followee = Profile.objects.get(pk=self.kwargs['pk'])
        except Profile.DoesNotExist:
            raise NotFound('There is no profile with given ID.')

        if not follower.is_following(followee):
            raise ValidationError('You do not follow profile with given ID yet.')

        follower.unfollow(followee)
        serializer = self.serializer_class(followee, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
