from django.db import models
from django.contrib.auth.models import User
from buyers.models import Buyer
from categories.models import Category
from colors.models import Color

from django.core.exceptions import ValidationError



class Flower(models.Model):
    FlowerMalik = models.CharField(max_length=50, blank=True, null=True,unique=False)

    title = models.CharField(max_length=50, unique=True)
    content = models.TextField()
    image = models.URLField(max_length=500, blank=True, null=True) 
    category = models.ManyToManyField(Category)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ManyToManyField(Color)
    available = models.IntegerField()
    price = models.FloatField()

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")

    def __str__(self):
        return self.title

    class Meta:
        # unique_together = ('title', 'category')
        # unique ='title'
        verbose_name_plural = "Flowers"





STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)  # User is already the reviewer
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices=STAR_CHOICES, max_length=10)

    def __str__(self):
        return f"Reviewer: {self.reviewer.first_name}; Flower: {self.flower.title}"  # Updated

    class Meta:
        verbose_name_plural = "Reviews"


