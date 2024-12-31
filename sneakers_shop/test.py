from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)
