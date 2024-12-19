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

# from rest_framework import serializers
# from .models import Flower
# from categories.models import Category
# from colors.models import Color

# class FlowerSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(many=False, read_only=True)  # Read-only for user display
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
#     color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), many=True)

#     class Meta:
#         model = Flower
#         fields = '__all__'
#         extra_kwargs = {
#             'title': {'required': True},
#             'content': {'required': True},
#             'image': {'required': True},
#             'available': {'required': True, 'min_value': 0},
#             'price': {'required': True, 'min_value': 0.0},
#         }

    

# from rest_framework import serializers
# from .models import Flower

# class FlowerSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(many=False)  # Display user as a string (e.g., username)
#     category = serializers.SerializerMethodField()  # Custom field for category names
#     color = serializers.SerializerMethodField()     # Custom field for color names

#     class Meta:
#         model = Flower
#         fields = '__all__'

#     def get_category(self, obj):
#         """Get the names of all categories associated with the flower."""
#         return [category.name for category in obj.category.all()]

#     def get_color(self, obj):
#         """Get the names of all colors associated with the flower."""
#         return [color.name for color in obj.color.all()]

# from rest_framework import serializers
# from . import models

# class FlowerSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(many=False)
#     category = serializers.StringRelatedField(many=True)
#     color = serializers.StringRelatedField(many=True)
#     class Meta:
#         model = models.Flower
#         fields = '__all__'





# from . import models
# class ReviewSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = models.Review
#         fields = '__all__'


from . import models
class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.CharField(source='reviewer.first_name', read_only=True)  # Corrected
    flower = serializers.CharField(source='flower.title', read_only=True)  # Corrected

    class Meta:
        # model = models.Review
        model = models.Review
        fields = '__all__'

    