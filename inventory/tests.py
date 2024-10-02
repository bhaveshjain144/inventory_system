from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class ItemTests(APITestCase):
    def test_create_item(self):
        url = reverse('item-list')
        data = {'name': 'NewItem', 'description': 'A new item'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
