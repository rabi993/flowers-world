from rest_framework import serializers
from .models import Flower
from categories.models import Category
from colors.models import Color

class FlowerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False, read_only=True)  # Display user as a string (e.g., username)
    
    # Show category and color names while allowing edits via IDs
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name',  # Use the name field for display
        many=True
    )
    color = serializers.SlugRelatedField(
        queryset=Color.objects.all(),
        slug_field='name',  # Use the name field for display
        many=True
    )

    class Meta:
        model = Flower
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},
            'content': {'required': True},
            'image': {'required': True},
            'available': {'required': True, 'min_value': 0},
            'price': {'required': True, 'min_value': 0.0},
        }




from . import models
class ReviewSerializer(serializers.ModelSerializer):
    # reviewer = serializers.CharField(source='reviewer.first_name', read_only=True)  # Corrected
    # flower = serializers.CharField(source='flower.title', read_only=True)  # Corrected

    class Meta:
        # model = models.Review
        model = models.Review
        fields = '__all__'

    