from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, LikeSerializer
from .services import filter_posts


class PostAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def get_queryset(self):
        return filter_posts(author__user__id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'user_id': self.request.user.id
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailAPIView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = PostSerializer
    queryset = filter_posts()


class PostLike(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        context = {
            'user_id': self.request.user.id,
            'post_id': self.kwargs['pk'],
            'like': True
        }

        serializer = self.serializer_class(
            data=request.data,
            context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostUnlike(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        context = {
            'user_id': self.request.user.id,
            'post_id': self.kwargs['pk'],
            'like': False
        }

        serializer = self.serializer_class(
            data=request.data,
            context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
