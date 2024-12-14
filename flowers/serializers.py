from rest_framework import serializers
from . import models

class FlowerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=True)
    color = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.Flower
        fields = '__all__'

# class ReviewSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.Review
#         fields = '__all__'

# class ReviewSerializer(serializers.ModelSerializer):
#     reviewer = serializers.CharField(source='reviewer.user.first_name', read_only=True)
#     flower= serializers.CharField(source='flower.title', read_only=True)

#     class Meta:
#         model = models.Review
#         fields = '__all__'
class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.CharField(source='reviewer.first_name', read_only=True)  # Corrected
    flower = serializers.CharField(source='flower.title', read_only=True)  # Corrected

    class Meta:
        model = models.Review
        fields = '__all__'