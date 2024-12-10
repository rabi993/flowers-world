from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers

class ServiceViewset(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

# from rest_framework.generics import ListAPIView
# from .models import Service
# from .serializers import ServiceSerializer

# class ServiceList(ListAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer

