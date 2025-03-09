from rest_framework import serializers
from .models import Newsletter

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

    def validate_cusEmail(self, value):
        if Newsletter.objects.filter(cusEmail=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value