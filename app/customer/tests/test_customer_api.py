"""
Tests for Customer APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Customer

from customer.serializers import (
    CustomerSerializer,
    CustomerDetailSerializer,
)


CUSTOMER_URL = reverse('customer:customer-list')


def detail_url(customer_id):
    """Create and return a customer detail URL."""
    return reverse('customer:customer-detail', args=[customer_id])


def create_customer(user, **params):
    """Create and return a sample customer."""
    defaults = {
        'name': 'John Doe',
        'phone_country': '+1',
        'phone_area': '202',
        'phone_code1': '555',
        'phone_code2': '0033',
        'email': 'john.doe@example.com',
    }
    defaults.update(params)

    customer = Customer.objects.create(user=user, **defaults)
    return customer


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicCustomerAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth us required to call API."""
        res = self.client.get(CUSTOMER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCustomerAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_customers(self):
        """Test retrieving a list of customers."""
        create_customer(user=self.user)
        create_customer(user=self.user)

        res = self.client.get(CUSTOMER_URL)

        customers = Customer.objects.all().order_by('-id')
        serializer = CustomerSerializer(customers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_customer_list_limited_to_user(self):
        """Tesst list of customers is limited to authenticated user."""
        other_user = create_user(email='other@example.com',
                                 password='password123')
        create_customer(user=other_user)
        create_customer(user=self.user)

        res = self.client.get(CUSTOMER_URL)

        customers = Customer.objects.filter(user=self.user)
        serializer = CustomerSerializer(customers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_customer_detail(self):
        """Test get customer detail."""
        customer = create_customer(user=self.user)

        url = detail_url(customer.id)
        res = self.client.get(url)

        serializer = CustomerDetailSerializer(customer)
        self.assertEqual(res.data, serializer.data)

    def test_create_customer(self):
        """Test creating a customer thru API"""
        payload = {
            'name': 'John Doe',
            'phone_country': '+1',
            'phone_area': '202',
            'phone_code1': '555',
            'phone_code2': '0033',
            'email': 'john.doe@example.com',
        }
        # POST /api/customers/customer
        res = self.client.post(CUSTOMER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(customer, k), v)
        self.assertEqual(customer.user, self.user)

    def test_partial_update(self):
        """Test partial update of a customer"""
        original_country = '+1'
        customer = create_customer(
            user=self.user,
            name='John Doe',
            phone_country=original_country,
            phone_area='202',
            phone_code1='555',
            phone_code2='0033',
            email='john.doe@example.com',
        )

        payload = {'name': 'Maria Antonieta'}
        url = detail_url(customer.id)
        # PATCH /api/customers/customer
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.name, payload['name'])
        self.assertEqual(customer.phone_country, original_country)
        self.assertEqual(customer.user, self.user)

    def test_full_update(self):
        """Test full update of a customer"""
        customer = create_customer(
            user=self.user,
            name='John Doe',
            phone_country='+1',
            phone_area='202',
            phone_code1='555',
            phone_code2='0033',
            email='john.doe@example.com',
        )

        payload = {
            'name': 'Maria Antonieta',
            'phone_country': '+351',
            'phone_area': '203',
            'phone_code1': '666',
            'phone_code2': '4444',
            'email': 'maria.antonieta@example.com',
        }

        url = detail_url(customer.id)
        # PUT /api/customers/customer
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(customer, k), v)
        self.assertEqual(customer.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the customer user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        customer = create_customer(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(customer.id)
        self.client.patch(url, payload)

        customer.refresh_from_db()
        self.assertEqual(customer.user, self.user)

    def test_delete_customer(self):
        """Test deleting customer sucessfully"""
        customer = create_customer(user=self.user)

        url = detail_url(customer.id)
        # DELETE /api/customers/customer
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(id=customer.id).exists())

    def test_customer_other_users_customer_error(self):
        """Test trying to delete another user customer gives error"""
        new_user = create_user(email='user2@example.com', password='test123')
        customer = create_customer(user=new_user)

        url = detail_url(customer.id)
        # DELETE /api/customers/customer
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Customer.objects.filter(id=customer.id).exists())

    def test_filter_by_phone_area(self):
        """Test filtering customers by Phone Area"""
        c1 = create_customer(
            user=self.user,
            name='Mary Briggs',
            phone_country='+1',
            phone_area='201',
            phone_code1='666',
            phone_code2='0045',
            email='mary.briggs@example.com',
        )
        c2 = create_customer(
            user=self.user,
            name='Mr Ed',
            phone_country='+1',
            phone_area='202',
            phone_code1='888',
            phone_code2='0034',
            email='mr.ed@example.com',
        )
        c3 = create_customer(
            user=self.user,
            name='John Doe',
            phone_country='+1',
            phone_area='203',
            phone_code1='555',
            phone_code2='0033',
            email='john.doe@example.com',
        )

        params = {'phone_area': {'202', '203'}}
        res = self.client.get(CUSTOMER_URL, params)

        s1 = CustomerSerializer(c1)
        s2 = CustomerSerializer(c2)
        s3 = CustomerSerializer(c3)

        self.assertNotIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertIn(s3.data, res.data)

    def test_filter_by_phone_country(self):
        """Test filtering customers by Phone Country"""
        c1 = create_customer(
            user=self.user,
            name='Mary Briggs',
            phone_country='+1',
            phone_area='201',
            phone_code1='666',
            phone_code2='0045',
            email='mary.briggs@example.com',
        )
        c2 = create_customer(
            user=self.user,
            name='Mr Ed',
            phone_country='+351',
            phone_area='202',
            phone_code1='888',
            phone_code2='0034',
            email='mr.ed@example.com',
        )
        c3 = create_customer(
            user=self.user,
            name='John Doe',
            phone_country='+44',
            phone_area='203',
            phone_code1='555',
            phone_code2='0033',
            email='john.doe@example.com',
        )

        params = {'phone_country': {'+44'}}
        res = self.client.get(CUSTOMER_URL, params)

        s1 = CustomerSerializer(c1)
        s2 = CustomerSerializer(c2)
        s3 = CustomerSerializer(c3)

        self.assertNotIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)
        self.assertIn(s3.data, res.data)
