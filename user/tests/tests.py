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
            "first_name": "Bob",
            "last_name": "Sallo",
            "phone": "+380999999999",
            "birth_date": "2000-01-01",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            get_user_model().objects.filter(email=payload["email"]).exists()
        )
        user = get_user_model().objects.get(email=payload["email"])
        self.assertEqual(user.first_name, payload["first_name"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(user.last_name, payload["last_name"])
        self.assertEqual(user.phone, payload["phone"])

    def test_me_requires_auth(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_missing_last_name_field(self):
        payload = {
            "email": "test1@gmail.com",
            "password": "testpassword123",
            "first_name": "Bob",
            "phone": "+380999999999",
            "birth_date": "2000-01-01",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticatedUserApiTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test1@gmail.com",
            password="testpassword123",
            first_name="Bob",
            last_name="Sallo",
            phone="+380999999999",
            birth_date="2000-01-01",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_me_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user.email)
        self.assertEqual(res.data["first_name"], self.user.first_name)
        self.assertEqual(res.data["phone"], self.user.phone)
