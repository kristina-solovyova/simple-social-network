from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from .models import Like, Post


def like_post(post_id, profile_id):
    try:
        post = Post.objects.get(pk=post_id)
    except ObjectDoesNotExist:
        raise NotFound('There is no post with given ID.')

    return Like.objects.update_or_create(
        profile_id=profile_id, post_id=post.id,
        defaults={'is_deleted': False},
    )


def unlike_post(post_id, profile_id):
    try:
        like = Like.objects.get(profile__pk=profile_id, post__pk=post_id, is_deleted=False)
        like.is_deleted = True
        like.save()
    except ObjectDoesNotExist:
        raise NotFound('You have not liked this post yet.')
    return like


def filter_posts(**filter_params):
    return Post.objects.filter(**filter_params)
