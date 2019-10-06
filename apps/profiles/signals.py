from django.db.models.signals import post_save
from django.dispatch import receiver
from social_net import settings
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
