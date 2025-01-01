
from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer


from django.shortcuts import get_object_or_404
from rest_framework import  status
from rest_framework.response import Response
# from . import models
# from . import serializers
from flowers.models import Flower
from buyers.models import Buyer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        
        queryset = super().get_queryset()

        # Extract query parameters
        flower_id = self.request.query_params.get('flower_id')
        buyer_id = self.request.query_params.get('buyer_id')

        # Filter by flower_id if provided
        if flower_id:
            queryset = queryset.filter(flower_id=flower_id)

        # Filter by buyer_id if provided
        if buyer_id:
            queryset = queryset.filter(buyer_id=buyer_id)

        return queryset

    def create(self, request, *args, **kwargs):
        
        # Get query parameters
        flower_id = self.request.query_params.get('flower_id')
        buyer_id = self.request.query_params.get('buyer_id')

        # Validate presence of both flower_id and buyer_id
        if not flower_id or not buyer_id:
            return Response(
                {"error": "Both 'flower_id' and 'buyer_id' must be provided in the query parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get Flower and Buyer objects or return 404 if not found
        flower = get_object_or_404(Flower, id=flower_id)
        buyer = get_object_or_404(Buyer, id=buyer_id)

        # Validate stock availability
        quantity = request.data.get('quantity', 1)
        if flower.available < int(quantity):
            return Response(
                {"error": f"Only {flower.available} units of '{flower.title}' are available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Automatically assign flower and buyer
        serializer.save(flower=flower, buyer=buyer)

        # Update flower stock
        flower.available += int(quantity)
        flower.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


