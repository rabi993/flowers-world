
from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from . import models
from . import serializers

class CategoryViewset(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer