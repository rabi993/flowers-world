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
    
class ReviewViewset(viewsets.ModelViewSet):
    
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer