"""
Serializers for the Customer APIs
"""
from rest_framework import serializers

from core.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customers."""

    class Meta:
        model = Customer
        fields = ('id',
                  'name',
                  'phone_country',
                  'phone_area',
                  'phone_code1',
                  'phone_code2'
                  )
        read_only_fields = ('id',)


class CustomerDetailSerializer(CustomerSerializer):
    """Serializer for Customer detail view"""

    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields + ('email',)
