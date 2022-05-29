"""
Views for the Customer APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Customer
from customer import serializers


class CustomerViewSet(viewsets.ModelViewSet):
    """View for manage customer APIs."""
    serializer_class = serializers.CustomerDetailSerializer
    queryset = Customer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve customers for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.CustomerSerializer

        if self.action == 'detail':
            return serializers.CustomerDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new customer"""
        serializer.save(user=self.request.user)
