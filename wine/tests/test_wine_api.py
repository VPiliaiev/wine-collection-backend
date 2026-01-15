from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from wine.models import Wine, Country, WineType, Category, Purpose, Mood


class WineListAPITest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Italy")
        self.wine_type = WineType.objects.create(name="white")
        self.category = Category.objects.create(name="classic")
        self.purpose = Purpose.objects.create(name="celebration")

        self.wine = Wine.objects.create(
            name="TestName",
            volume=0.75,
            price=10,
            country=self.country,
            wine_type=self.wine_type,
            category=self.category,
            purpose=self.purpose,
            stock=5,
        )

    def test_wine_list(self):
        url = reverse("wine:wine-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

        wine_data = response.data["results"][0]
        self.assertEqual(wine_data["name"], "TestName")
        self.assertIn("image", wine_data)


class WineDetailAPITest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Italy")
        self.wine_type = WineType.objects.create(name="white")
        self.category = Category.objects.create(name="classic")
        self.purpose = Purpose.objects.create(name="celebration")

        self.wine = Wine.objects.create(
            name="Odulin",
            volume=0.75,
            price=10,
            description="Test description",
            country=self.country,
            wine_type=self.wine_type,
            category=self.category,
            purpose=self.purpose,
            stock=5,
        )

    def test_wine_detail(self):
        url = reverse("wine:wine-detail", args=[self.wine.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.wine.id)
        self.assertEqual(response.data["name"], "Odulin")
        self.assertEqual(response.data["price"], "10.00")
        self.assertEqual(response.data["stock"], 5)
        self.assertTrue(response.data["in_stock"])


class WineFilterAPITest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Italy")
        self.wine_type = WineType.objects.create(name="white")
        self.category_classic = Category.objects.create(name="classic")
        self.category_premium = Category.objects.create(name="premium")

        self.purpose_gift = Purpose.objects.create(name="gift")
        self.purpose_party = Purpose.objects.create(name="party")

        self.mood_romantic = Mood.objects.create(name="romantic")
        self.mood_festive = Mood.objects.create(name="festive")

        self.wine1 = Wine.objects.create(
            name="Odulin White",
            volume=0.75,
            price=10,
            country=self.country,
            wine_type=self.wine_type,
            category=self.category_classic,
            purpose=self.purpose_gift,
            stock=5,
        )
        self.wine1.moods.add(self.mood_romantic)

        self.wine2 = Wine.objects.create(
            name="Bellevue Premium",
            volume=0.75,
            price=25,
            country=self.country,
            wine_type=self.wine_type,
            category=self.category_premium,
            purpose=self.purpose_party,
            stock=3,
        )
        self.wine2.moods.add(self.mood_festive)

        self.url = reverse("wine:wine-list")

    def test_filter_by_name(self):
        response = self.client.get(self.url, {"name": "odulin"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Odulin White")

    def test_filter_by_mood(self):
        response = self.client.get(self.url, {"mood": "romantic"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Odulin White")

    def test_filter_by_price_range(self):
        response = self.client.get(self.url, {"min_price": 20, "max_price": 30})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Bellevue Premium")

    def test_filter_by_category(self):
        response = self.client.get(self.url, {"category": "classic"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Odulin White")

    def test_filter_by_purpose(self):
        response = self.client.get(self.url, {"purpose": "gift"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Odulin White")

    def test_filter_by_country(self):
        response = self.client.get(self.url, {"country": "Italy"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_combined_filters(self):
        response = self.client.get(
            self.url,
            {
                "purpose": "party",
                "min_price": 20,
                "category": "premium",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Bellevue Premium")
