from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    posts_num = serializers.SerializerMethodField(read_only=True)
    follows_me = serializers.SerializerMethodField()
    am_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'full_name', 'birthday', 'bio', 'follows_me',
                  'am_following', 'location', 'timeZone', 'site', 'posts_num')
        read_only_fields = ['user', 'follows_me', 'am_following', 'posts_num']

    def get_posts_num(self, profile):
        return profile.posts.count()

    def get_follows_me(self, profile):
        user = self.context['request'].user
        current_profile = user.profile
        return current_profile.is_followed_by(profile)

    def get_am_following(self, profile):
        user = self.context['request'].user
        current_profile = user.profile
        return current_profile.is_following(profile)
