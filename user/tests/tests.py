from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

CREATE_USER_URL = reverse("user:create")
ME_URL = reverse("user:manage_user")


class UnauthenticatedUserApiTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            "email": "test@gmail.com",
            "password": "testpassword123",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            get_user_model().objects.filter(email=payload["email"]).exists()
        )

    def test_me_requires_auth(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserApiTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="testpassword123",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_me_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user.email)
