from django.db import models

# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)


    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Colors"