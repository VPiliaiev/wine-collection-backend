from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from cart.models import Cart
from wine.models import Country, WineType, Category, Purpose, Wine

User = get_user_model()


def sample_wine(**params):
    country, _ = Country.objects.get_or_create(name="Spain")
    wine_type, _ = WineType.objects.get_or_create(name="Red")
    category, _ = Category.objects.get_or_create(name="Classic")
    purpose, _ = Purpose.objects.get_or_create(name="Party")

    defaults = {
        "name": "Test Wine",
        "volume": 0.75,
        "price": 500.00,
        "country": country,
        "wine_type": wine_type,
        "category": category,
        "purpose": purpose,
        "stock": 10,
    }
    defaults.update(params)
    return Wine.objects.create(**defaults)


class UnauthenticatedCartApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.wine = sample_wine()
        self.list_url = reverse("cart:cart-list")
        self.add_url = reverse("cart:cart-add-item")

    def test_get_empty_cart(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], None)

    def test_add_item_in_cart(self):
        payload = {"wine": self.wine.id, "quantity": 2}
        res = self.client.post(self.add_url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["items"][0]["wine_id"], self.wine.id)
        self.assertEqual(res.data["items"][0]["quantity"], 2)

    def test_update_quantity_item(self):
        setup_res = self.client.post(
            self.add_url, {"wine": self.wine.id, "quantity": 1}
        )
        cart_id = setup_res.data["id"]

        url = reverse("cart:cart-update-quantity")
        full_url = f"{url}?cart_id={cart_id}&wine_id={self.wine.id}&quantity=5"

        res = self.client.patch(full_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["items"][0]["quantity"], 5)

    def test_remove_one_item_from_cart(self):
        setup_res = self.client.post(
            self.add_url, {"wine": self.wine.id, "quantity": 2}
        )
        cart_id = setup_res.data["id"]

        url = reverse("cart:cart-remove-one")
        full_url = f"{url}?cart_id={cart_id}&wine_id={self.wine.id}"

        res = self.client.delete(full_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["items"][0]["quantity"], 1)

    def test_clear_all_cart(self):
        setup_res = self.client.post(
            reverse("cart:cart-add-item"), {"wine": self.wine.id, "quantity": 1}
        )
        cart_id = setup_res.data["id"]

        clear_url = reverse("cart:cart-clear")
        res = self.client.delete(f"{clear_url}?cart_id={cart_id}")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["items"]), 0)

    def test_stock_validation(self):
        payload = {"wine": self.wine.id, "quantity": 15}
        res = self.client.post(self.add_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("non_field_errors" in res.data or "error" in res.data)


class AuthenticatedCartTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@test.com", password="password123"
        )
        self.client.force_authenticate(self.user)
        self.wine = sample_wine()
        self.add_url = reverse("cart:cart-add-item")

    def test_auth_user_cart_creation(self):
        self.client.post(self.add_url, {"wine": self.wine.id, "quantity": 1})
        res = self.client.get(reverse("cart:cart-list"))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["items"][0]["wine_id"], self.wine.id)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)

    def test_merge_carts(self):
        anon_client = APIClient()
        setup_res = anon_client.post(
            self.add_url, {"wine": self.wine.id, "quantity": 3}
        )
        anon_cart_id = setup_res.data["id"]

        merge_url = reverse("cart:cart-merge-unauthorized-cart-to-user")
        res = self.client.post(f"{merge_url}?cart_id={anon_cart_id}")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["items"][0]["quantity"], 3)
        self.assertFalse(Cart.objects.filter(id=anon_cart_id).exists())
