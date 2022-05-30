"""
Test for the health check API
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

URL_HEALTH = 'health-check'


class HealthCheckTests(TestCase):
    """Test the health check API"""

    def test_health_check(self):
        """Test health check API."""
        client = APIClient()
        url = reverse(URL_HEALTH)
        res = client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
