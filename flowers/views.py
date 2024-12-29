from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import filters, pagination
# from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
# from rest_framework.permissions import BasePermission

# Create your views here.
class FlowerPagination(pagination.PageNumberPagination):
    page_size = 10 # items per page
    page_size_query_param = page_size
    max_page_size = 100

# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import  status

class FlowerViewset(viewsets.ModelViewSet):
    queryset = models.Flower.objects.all()
    serializer_class = serializers.FlowerSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = FlowerPagination
    search_fields = ['title', 'content', 'category__name', 'color__name']
    # permission_classes = [IsAuthenticatedOrReadOnly]




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
    

