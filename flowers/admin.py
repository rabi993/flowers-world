from django.contrib import admin

# Register your models here.
from . import models


admin.site.register(models.Flower)
admin.site.register(models.Review)