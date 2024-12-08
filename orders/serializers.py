from rest_framework import serializers
from . import models

class OrderSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(many=False)
    doctor = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Order
        fields = '__all__'




# from rest_framework import serializers
# from .models import Order

# class OrderSerializer(serializers.ModelSerializer):
#     buyer_name = serializers.ReadOnlyField(source='buyer.user.get_full_name')  # Auto-filled
#     flower_title = serializers.ReadOnlyField(source='flower.title')  # Auto-filled

#     class Meta:
#         model = Order
#         fields = ['id', 'buyer_name', 'flower_title', 'quantity', 'delivery_address', 'mobile_no', 'email', 'order_date','delivery_date', 'status']
#         read_only_fields = ['buyer_name', 'flower_title', 'status', 'order_date', 'delivery_date']
    
#     def validate_quantity(self, value):
#         flower = self.context['flower']
#         if flower.available < value:
#             raise serializers.ValidationError(f"Only {flower.available} items are available.")
#         return value

#     def create(self, validated_data):
#         flower = self.context['flower']
#         quantity = validated_data['quantity']
        
#         # Reduce flower stock
#         flower.available -= quantity
#         flower.save()
        
#         # Save order
#         return Order.objects.create(**validated_data, buyer=self.context['buyer'], flower=flower)
