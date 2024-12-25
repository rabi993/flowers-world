import requests
from rest_framework import serializers
from . import models

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'
    
    # def create(self, validated_data):
    #     # Extract image from the request
    #     image_file = self.context['request'].FILES.get('image')  # Expecting an image in the 'image' field
    #     if image_file:
    #         # Upload the image to ImgBB
    #         try:
    #             image_url = self.upload_to_imgbb(image_file)
    #             validated_data['image'] = image_url  # Save the ImgBB URL in the model
    #         except Exception as e:
    #             raise serializers.ValidationError(f"Image upload failed: {e}")
    #     return super().create(validated_data)

    # def upload_to_imgbb(self, image):
    #     API_KEY = '6b0c007afbf8da08520a75fb493991aa'  
    #     url = 'https://api.imgbb.com/1/upload'

    #     # Prepare the payload
    #     payload = {'key': API_KEY}
    #     files = {'image': image}

    #     # Send the POST request
    #     response = requests.post(url, data=payload, files=files)
    #     if response.status_code == 200:
    #         # Return the image URL from ImgBB response
    #         print(response.json()['data']['url'])
    #         return response.json()['data']['url']
    #     # Handle API errors
    #     raise serializers.ValidationError("Failed to upload image to ImgBB. Please try again.")