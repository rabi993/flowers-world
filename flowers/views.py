from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import filters, pagination
# from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
# from rest_framework.permissions import BasePermission

# Create your views here.
class FlowerPagination(pagination.PageNumberPagination):
    page_size = 1 # items per page
    page_size_query_param = page_size
    max_page_size = 100

class FlowerViewset(viewsets.ModelViewSet):
    queryset = models.Flower.objects.all()
    serializer_class = serializers.FlowerSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = FlowerPagination
    search_fields = ['user__first_name', 'user__email', 'category__name', 'color__name']
    
# class ReviewViewset(viewsets.ModelViewSet):
    
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.ReviewSerializer


from rest_framework.response import Response

class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        """
        Custom queryset to filter reviews based on reviewer_id and flower_id.
        """
        queryset = super().get_queryset()
        reviewer_id = self.request.query_params.get('reviewer_id')
        flower_id = self.request.query_params.get('flower_id')

        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        if flower_id:
            queryset = queryset.filter(flower_id=flower_id)

        return queryset
    


# class ReviewFlowerIdViewset(viewsets.ModelViewSet):
#     serializer_class = serializers.ReviewSerializer

#     def get_queryset(self):
#         flower_id = self.request.query_params.get('flower_id', None)
#         if flower_id is not None:
#             return models.Review.objects.filter(flower__id=flower_id)
#         return models.Review.objects.all()

# class ReviewFlowerIdViewset(viewsets.ModelViewSet):
#     serializer_class = serializers.ReviewSerializer

#     def get_queryset(self):
#         # Default queryset (all reviews)
#         queryset = models.Review.objects.all()
#         flower_id = self.request.query_params.get('flower_id', None)
#         if flower_id is not None:
#             # Filter reviews by flower_id
#             queryset = queryset.filter(flower__id=flower_id)
#         return queryset