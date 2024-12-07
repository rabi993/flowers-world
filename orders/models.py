from django.db import models
from buyers.models import Buyer
from flowers.models import Flower

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    delivery_address = models.TextField()
    mobile_no = models.CharField(max_length=12)
    delivery_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Default to pending

    def __str__(self):
        return f"Order by {self.buyer.user.first_name} for {self.flower.title} ({self.status})"
