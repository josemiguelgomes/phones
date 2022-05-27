"""
Unit tests for calc
"""
from django.test import SimpleTestCase

from app import calc

class CalculatorTests(SimpleTestCase):   
    """Test the calc module"""
    

    def test_add_positive_numbers(self):
        res = calc.add(1, 3)
        self.assertEqual(res, 4)

    def test_add_negative_numbers(self):
        res = calc.add(-1, -3)
        self.assertEqual(res, -4)

    def test_add_positive_negative_numbers(self):
        res = calc.add(3, -1)
        self.assertEqual(res, 2)

        
    

