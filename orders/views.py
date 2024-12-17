# http://127.0.0.1:8000/orders/?flower_id=&buyer_id=
# Filters based on both flower_id and buyer_id.

# http://127.0.0.1:8000/orders/?flower_id=
# Filters based on flower_id only.

# http://127.0.0.1:8000/orders/?buyer_id=
# Filters based on buyer_id only.

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
        """
        Custom queryset to filter orders based on query parameters.
        """
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
        """
        Override the create method to handle flower_id and buyer_id from query parameters.
        """
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
        # flower.available -= int(quantity)
        # flower.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



# from django.shortcuts import render
# from rest_framework import viewsets
# from . import models
# from . import serializers

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = models.Order.objects.all()
#     serializer_class = serializers.OrderSerializer

#     def get_queryset(self):
#         """
#         Custom queryset to filter orders based on query parameters.
#         """
#         queryset = super().get_queryset()
#         flower_id = self.request.query_params.get('flower_id')
#         buyer_id = self.request.query_params.get('buyer_id')

#         if flower_id:
#             queryset = queryset.filter(flower_id=flower_id)
#         if buyer_id:
#             queryset = queryset.filter(buyer_id=buyer_id)

#         return queryset


# from django.shortcuts import render
# from rest_framework import viewsets
# from . import models
# from . import serializers
# # Create your views here.
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = models.Order.objects.all()
#     serializer_class =  serializers.OrderSerializer
    
#     # custom query kortechi
#     def get_queryset(self):
#         queryset = super().get_queryset() # 7 no line ke niye aslam ba buyer ke inherit korlam
#         print(self.request.query_params)
#         buyer_id = self.request.query_params.get('buyer_id')
#         if buyer_id:
#             queryset = queryset.filter(buyer_id=buyer_id)
#         return queryset



# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from .models import Order
# from .serializers import OrderSerializer
# from buyers.models import Buyer
# from django.core.mail import send_mail

# from flowers.models import Flower

# class CreateOrderView(generics.CreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         flower = Flower.objects.get(pk=self.kwargs['flower_id'])  # Get flower from URL
#         buyer = Buyer.objects.get(user=self.request.user)  # Get logged-in user as buyer
#         context.update({'flower': flower, 'buyer': buyer})
#         return context

# # View order history for a logged-in user
# class UserOrderHistoryView(generics.ListAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         buyer = Buyer.objects.get(user=self.request.user)
#         return Order.objects.filter(buyer=buyer)


# # Admin view to manage orders
# class AdminOrderManagementView(generics.ListCreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAdminUser]

#     def get_queryset(self):
#         return Order.objects.all()

# # Update order status (admin only)
# class AdminUpdateOrderStatusView(generics.UpdateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAdminUser]
#     queryset = Order.objects.all()

#     def perform_update(self, serializer):
#         instance = serializer.save()
#         if instance.status == 'completed':
#             # Send confirmation email to the user
#             send_mail(
#                 'Order Confirmation',
#                 f'Your order for {instance.flower.title} has been confirmed.',
#                 'rabiulislam.170113@s.pust.ac.bd',  # From email
#                 [instance.email],  # To email
#                 fail_silently=False,
#             )
