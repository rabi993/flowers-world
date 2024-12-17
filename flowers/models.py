from django.db import models
from django.contrib.auth.models import User
from buyers.models import Buyer
from categories.models import Category
from colors.models import Color

from django.core.exceptions import ValidationError



class Flower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming a user can have multiple flowers
    title = models.CharField(max_length=50, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to="flowers/images/")
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


# class FlowerCategory(models.Model):
#     flower = models.ForeignKey('Flower', on_delete=models.CASCADE)
#     category = models.ForeignKey('Category', on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ['flower', 'category']

#     def __str__(self):
#         return f"{self.flower.title} - {self.category.name}"


# # Create your models here.

# class Flower(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE)
#     title = models.CharField(max_length=50)
#     content = models.TextField()
#     image = models.ImageField(upload_to="flowers/images/")
#     category = models.ManyToManyField(Category)
#     color =  models.ManyToManyField(Color)
#     available = models.IntegerField()
#     price = models.FloatField()
    
#     def __str__(self):
#         return self.title 
#     class Meta:
#         unique_together = ('title', 'category')
#         verbose_name_plural = "Flowers"

    
        
    
    # def decrease_available(self):
    #     if self.Available > 0:
    #         self.Available -= 1
    #         self.save()


# STAR_CHOICES = [
#     ('⭐', '⭐'),
#     ('⭐⭐', '⭐⭐'),
#     ('⭐⭐⭐', '⭐⭐⭐'),
#     ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
#     ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
# ]
# class Review(models.Model):
#     reviewer = models.ForeignKey(User, on_delete = models.CASCADE)
#     flower = models.ForeignKey(Flower, on_delete = models.CASCADE)
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add = True)
#     rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    
#     def __str__(self):
#         return f"Patient : {self.reviewer.user.first_name} ; Flower {self.flower.title}"
#     class Meta:
#         verbose_name_plural = "Reviews"


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


