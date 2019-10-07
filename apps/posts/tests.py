from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Post


class PostListCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('post-list')
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            username='testuser',
            password='password'
        )
        self.client.force_authenticate(user=self.user)

    def test_post_create_correct(self):
        data = {
            "text": "Test post #1 by user {}".format(self.user.username)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user.email, response.data['author'])

    def test_post_create_no_text(self):
        response = self.client.post(self.url, {})
        text_err = response.data['text']
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("This field is required.", text_err)

    def test_post_list(self):
        Post.objects.create(author=self.user.profile, text="Test text 1")
        Post.objects.create(author=self.user.profile, text="Test text 2")
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Post.objects.filter(author=self.user.profile).count(), response.data['count'])


class PostDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            username='testuser',
            password='password'
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.user.profile, text="Test text #1")
        self.url = reverse('post-detail', kwargs={"pk": self.post.pk})

    def test_get_post(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.post.text, response.data['text'])

    def test_post_delete_by_author(self):
        post = Post.objects.create(author=self.user.profile, text="Test text #2")
        url = reverse('post-detail', kwargs={"pk": post.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_post_delete_alien(self):
        other_user = get_user_model().objects.create_user(
            email='testuser2@test.com',
            username='testuser2',
            password='password'
        )
        post = Post.objects.create(author=other_user.profile, text="Test text #3")
        url = reverse('post-detail', kwargs={"pk": post.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post_delete_not_found(self):
        url = reverse('post-detail', kwargs={"pk": 666})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class LikesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            username='testuser',
            password='password'
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.user.profile, text="Test text #1")
        self.like_url = reverse('like-post', kwargs={"pk": self.post.pk})
        self.unlike_url = reverse('unlike-post', kwargs={"pk": self.post.pk})

    def test_post_like(self):
        response = self.client.post(self.like_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.post.pk, response.data['post'])
        self.assertEqual(self.user.email, response.data['profile'])
        self.assertTrue(response.data['liked'])

    def test_post_like_not_found(self):
        url = reverse('like-post', kwargs={"pk": 888})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_post_unlike(self):
        self.post.likes.create(profile=self.user.profile)
        response = self.client.post(self.unlike_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.post.pk, response.data['post'])
        self.assertEqual(self.user.email, response.data['profile'])
        self.assertFalse(response.data['liked'])

    def test_post_unlike_not_found(self):
        url = reverse('unlike-post', kwargs={"pk": 888})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
