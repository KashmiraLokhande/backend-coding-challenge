from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import City

class CitySuggestionsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test data
        City.objects.create(name="London", lat=42.98339, lon=-81.23304, country="CA")
        City.objects.create(name="London", lat=37.12898, lon=-84.08326, country="US")
        City.objects.create(name="London", lat=39.88645, lon=-83.44825, country="US")
        City.objects.create(name="Londontowne", lat=38.93345, lon=-76.54941, country="US")
        City.objects.create(name="New London", lat=44.39276, lon=-88.73983, country="US")

    def test_exact_match(self):
        url = reverse('suggestions')
        response = self.client.get(url, {"q": "London"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["suggestions"]), 5)
        self.assertEqual(data["suggestions"][0]["name"], "London, CA")
        self.assertAlmostEqual(data["suggestions"][0]["score"], 1.0, places=1)

    def test_prefix_match(self):
        url = reverse('suggestions')
        response = self.client.get(url, {"q": "Londont"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["suggestions"]), 1)
        self.assertEqual(data["suggestions"][0]["name"], "Londontowne, US")
        self.assertAlmostEqual(data["suggestions"][0]["score"], 0.7, places=1)

    def test_moderate_match(self):
        url = reverse('suggestions')
        response = self.client.get(url, {"q": "ntowne"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["suggestions"]), 1)
        self.assertEqual(data["suggestions"][-1]["name"], "Londontowne, US")
        self.assertAlmostEqual(data["suggestions"][-1]["score"], 0.5, places=1)

    def test_no_latitude_longitude(self):
        url = reverse('suggestions')
        response = self.client.get(url, {"q": "London"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["suggestions"]), 5)
        self.assertEqual(data["suggestions"][0]["name"], "London, CA")
        self.assertAlmostEqual(data["suggestions"][0]["score"], 1.0, places=1)

    def test_latitude_longitude_given(self):
        url = reverse('suggestions')
        response = self.client.get(url, {"q": "London", "latitude": 43.70011, "longitude": -79.4163})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["suggestions"]), 5)
        scores = [item["score"] for item in data["suggestions"]]
        self.assertEqual(scores, sorted(scores, reverse=True))
