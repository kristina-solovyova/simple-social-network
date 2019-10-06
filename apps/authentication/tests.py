import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signup')
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            username='testuser',
            password='password'
        )

    def tearDown(self):
        for user in get_user_model().objects.all():
            user.delete()

    def test_user_signup_correct(self):
        data = {
            "username": "user666",
            "email": "user666@gmail.com",
            "password": "password"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_user_signup_min_password_err(self):
        data = {
            "username": "user666",
            "email": "user666@gmail.com",
            "password": "pwd"
        }
        response = self.client.post(self.url, data)
        pwd_err = json.loads(response.content)['password'].pop()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("Ensure this field has at least 8 characters.", pwd_err)

    def test_signup_with_existing_user(self):
        data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "password"
        }
        response = self.client.post(self.url, data)
        exists_err = json.loads(response.content)['email'].pop()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("user with this email already exists.", exists_err)

    def test_signup_with_undeliverable_email(self):
        data = {
            "username": "testuser",
            "email": "testuser@kek.com",
            "password": "password"
        }
        response = self.client.post(self.url, data)
        email_err = json.loads(response.content)['email'].pop()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("This is undeliverable email. Please use another one.", email_err)


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            username='testuser',
            password='password'
        )

    def test_login_correct(self):
        data = {
            "email": "testuser@test.com",
            "password": "password"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("token", json.loads(response.content))

    def test_login_wrong_credentials(self):
        data = {
            "email": "testuser@test.com",
            "password": "password666"
        }
        response = self.client.post(self.url, data)
        non_field_errors = json.loads(response.content)['non_field_errors']
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("Unable to log in with provided credentials.", non_field_errors)

    def test_login_no_password(self):
        data = {
            "email": "testuser@test.com"
        }
        response = self.client.post(self.url, data)
        password = json.loads(response.content)['password']
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("This field is required.", password)
