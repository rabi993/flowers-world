from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length = 20)
    description = models.TextField()
    image = models.URLField(max_length=500, blank=True, null=True) 