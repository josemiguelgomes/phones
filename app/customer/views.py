"""
Views for the Customer APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Customer
from customer import serializers

from django.core.mail import send_mail


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'phone_area',
                OpenApiTypes.STR,
                description="Comma separated list of Phone Areas to filter",
            ),
            OpenApiParameter(
                'phone_country',
                OpenApiTypes.STR,
                description="Comma separated list of Phone Countries to filter",
            )
        ]
    )
)
class CustomerViewSet(viewsets.ModelViewSet):
    """View for manage customer APIs."""
    serializer_class = serializers.CustomerDetailSerializer
    queryset = Customer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve customers for authenticated user with
           filter on Phone Area and Phone Country."""
#       phone_area = self.request.query_params.get('phone_area')
        phone_area = self.request.query_params.getlist('phone_area')
        phone_country = self.request.query_params.getlist('phone_country')
        queryset = self.queryset
        if phone_area:
            queryset = queryset.filter(phone_area__in=phone_area)
        if phone_country:
            queryset = queryset.filter(phone_country__in=phone_country)

        queryset = queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

        """Emails to the first customer found in the search
           (if the search was done by phone_area"""
        first_element = queryset.all().first()
        if first_element is not None:
            send_mail('Test Subject',
                      'Here is the message',
                      'from@example.com',
                      [first_element.email],
                      fail_silently=False
                      )

        return queryset

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
