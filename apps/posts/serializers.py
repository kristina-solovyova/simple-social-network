from rest_framework import serializers
from apps.profiles.models import Profile
from .models import Post, Like
from .services import like_post, unlike_post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.user.email')
    likes_num = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'created', 'likes_num')
        read_only_fields = ['created', 'likes_num']

    def create(self, validated_data):
        user_id = self.context['user_id']
        profile = Profile.objects.get(user__pk=user_id)
        post = Post.objects.create(author=profile, **validated_data)
        return post

    def get_likes_num(self, post):
        return post.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.id')
    profile = serializers.ReadOnlyField(source='profile.user.email')
    time = serializers.ReadOnlyField(source='updated')

    class Meta:
        model = Like
        fields = ('profile', 'post', 'time')
        read_only_field = ['time']
        extra_kwargs = {'is_deleted': {'write_only': True}}

    def create(self, validated_data):
        user_id = self.context['user_id']
        profile = Profile.objects.get(user__pk=user_id)
        post_id = self.context['post_id']
        like = self.context['like']

        if like:
            obj, created = like_post(post_id, profile.id)
        else:
            obj = unlike_post(post_id, profile.id)

        return obj
