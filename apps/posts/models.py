from django.db import models


class Post(models.Model):
    # Fields
    author = models.ForeignKey(
        'profiles.Profile',
        related_name='posts',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Metadata
    class Meta:
        ordering = ["-created"]
        db_table = "posts"
        indexes = [
            models.Index(fields=['created'], name='created_post_idx'),
        ]

    # Methods
    def __str__(self):
        return str(self.id) + ': ' + self.author.user.email


class Like(models.Model):
    # Fields
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    profile = models.ForeignKey(
        'profiles.Profile',
        related_name='liked',
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Metadata
    class Meta:
        ordering = ["-updated"]
        db_table = "likes"
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='post_user_unq')
        ]
        indexes = [
            models.Index(fields=['updated'], name='updated_like_idx'),
        ]

    # Methods
    def __str__(self):
        return 'Like #%d by user %s on post %d' % (self.id, self.profile.user.email, self.post.id)
