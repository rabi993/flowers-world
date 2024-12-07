from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order
from .serializers import OrderSerializer
from buyers.models import Buyer
from django.core.mail import send_mail

from flowers.models import Flower

class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        flower = Flower.objects.get(pk=self.kwargs['flower_id'])  # Get flower from URL
        buyer = Buyer.objects.get(user=self.request.user)  # Get logged-in user as buyer
        context.update({'flower': flower, 'buyer': buyer})
        return context

# View order history for a logged-in user
class UserOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        buyer = Buyer.objects.get(user=self.request.user)
        return Order.objects.filter(buyer=buyer)


# Admin view to manage orders
class AdminOrderManagementView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Order.objects.all()

# Update order status (admin only)
class AdminUpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'completed':
            # Send confirmation email to the user
            send_mail(
                'Order Confirmation',
                f'Your order for {instance.flower.title} has been confirmed.',
                'rabiulislam.170113@s.pust.ac.bd',  # From email
                [instance.email],  # To email
                fail_silently=False,
            )
