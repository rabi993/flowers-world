from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from . import models
from . import serializers

class NewsletterViewset(viewsets.ModelViewSet):
    queryset = models.Newsletter.objects.all()
    serializer_class = serializers.NewsletterSerializer