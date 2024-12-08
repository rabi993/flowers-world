from django.db import models
from buyers.models import Buyer
from flowers.models import Flower
from django.utils.timezone import now

ORDER_STATUS = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
]
ORDER_TYPES = [
    ('Offline', 'Offline'),
    ('Online', 'Online'),
]

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    delivery_address = models.TextField()
    mobile_no = models.CharField(max_length=12)
    order_date = models.DateTimeField(default=now)
    delivery_date = models.DateField()
    order_types = models.CharField(choices = ORDER_TYPES, max_length = 10, default='Online')
    order_status = models.CharField(choices = ORDER_STATUS, max_length = 10, default = "Pending")
    cancel = models.BooleanField(default = False)

    def __str__(self):
        return f"Flower : {self.flower.title}, Buyer : {self.buyer.user.first_name}"
    
