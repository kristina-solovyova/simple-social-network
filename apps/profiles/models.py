from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False
    )
    location = models.CharField(blank=True, max_length=255)
    timeZone = models.CharField(blank=True, max_length=127)
    site = models.CharField(blank=True, max_length=127)

    class Meta:
        db_table = "profiles"

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        """Follow `profile` if not already"""
        self.following.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if already following."""
        self.following.remove(profile)
