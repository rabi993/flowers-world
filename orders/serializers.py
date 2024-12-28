from rest_framework import serializers
from . import models

class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(many=False)
    flower = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Order
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


