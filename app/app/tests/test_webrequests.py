"""
Unit tests for webrequests
"""
from django.test import SimpleTestCase
from rest_framework.test import APIClient


class TestViews(SimpleTestCase):

    def test_get_greetings(self):
        """Test GET greetings"""
        client = APIClient()
        res = client.get('/greetings/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.data,
            ["Hello!", "Bonjour!", "Olá!"],
        )
