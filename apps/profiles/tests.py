from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class ProfileDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            username='testuser',
            password='password'
        )
        self.profile = self.user.profile
        self.client.force_authenticate(user=self.user)
        self.url = reverse('profile-detail', kwargs={"pk": self.profile.pk})

    def test_get_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.email, response.data['user'])

    def test_get_profile_not_found(self):
        url = reverse('profile-detail', kwargs={"pk": 666})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_profile(self):
        data = {
            "full_name": "John Doe",
            "bio": "I am very good person"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['full_name'], response.data['full_name'])

    def test_update_profile_alien(self):
        other_user = get_user_model().objects.create_user(
            email='testuser2@test.com',
            username='testuser2',
            password='password'
        )
        url = reverse('profile-detail', kwargs={"pk": other_user.profile.pk})
        response = self.client.put(url, {})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_profile_not_found(self):
        url = reverse('profile-detail', kwargs={"pk": 666})
        response = self.client.put(url, {})
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class ProfileFollowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            username='testuser',
            password='password'
        )
        self.client.force_authenticate(user=self.user)
        self.profile = self.user.profile
        self.other_user = get_user_model().objects.create_user(
            email='testuser2@test.com',
            username='testuser2',
            password='password'
        )
        self.other_profile = self.other_user.profile

    def test_profile_follow(self):
        url = reverse('follow-profile', kwargs={"pk": self.other_profile.pk})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.other_user.email, response.data['user'])
        self.assertTrue(response.data['am_following'])

    def test_profile_follow_not_found(self):
        url = reverse('follow-profile', kwargs={"pk": 666})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_profile_follow_yourself(self):
        url = reverse('follow-profile', kwargs={"pk": self.profile.pk})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("You can not follow yourself.", response.data)

    def test_profile_follow_twice(self):
        self.profile.follow(self.other_profile)
        url = reverse('follow-profile', kwargs={"pk": self.other_profile.pk})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("You are already following profile with given ID.", response.data)

    def test_profile_unfollow(self):
        self.profile.follow(self.other_profile)
        url = reverse('unfollow-profile', kwargs={"pk": self.other_profile.pk})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.other_user.email, response.data['user'])
        self.assertFalse(response.data['am_following'])

    def test_profile_unfollow_not_followed(self):
        url = reverse('unfollow-profile', kwargs={"pk": self.other_profile.pk})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("You do not follow profile with given ID yet.", response.data)

    def test_profile_unfollow_not_found(self):
        url = reverse('unfollow-profile', kwargs={"pk": 666})
        response = self.client.post(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
