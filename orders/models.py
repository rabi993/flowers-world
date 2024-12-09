# from django.db import models
# from buyers.models import Buyer
# from flowers.models import Flower
# from django.utils.timezone import now

# ORDER_STATUS = [
#     ('Completed', 'Completed'),
#     ('Pending', 'Pending'),
#     ('Processing', 'Processing'),
# ]
# ORDER_TYPES = [
#     ('Offline', 'Offline'),
#     ('Online', 'Online'),
# ]

# class Order(models.Model):
#     buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
#     flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     delivery_address = models.TextField()
#     mobile_no = models.CharField(max_length=12)
#     order_date = models.DateTimeField(default=now)
#     delivery_date = models.DateField()
#     order_types = models.CharField(choices = ORDER_TYPES, max_length = 10, default='Online')
#     order_status = models.CharField(choices = ORDER_STATUS, max_length = 10, default = "Pending")
#     cancel = models.BooleanField(default = False)

#     def __str__(self):
#         return f"Flower : {self.flower.title}, Buyer : {self.buyer.user.first_name}"
    
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from buyers.models import Buyer
from flowers.models import Flower

ORDER_STATUS = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Completed', 'Completed'),
]
ORDER_TYPES = [
    ('Online', 'Online'),
    ('Offline', 'Offline'),
]

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    delivery_address = models.TextField()
    mobile_no = models.CharField(max_length=12)
    order_date = models.DateTimeField(default=now)
    delivery_date = models.DateField()
    order_types = models.CharField(choices=ORDER_TYPES, max_length=10, default='Online')
    order_status = models.CharField(choices=ORDER_STATUS, max_length=10, default="Pending")
    cancel = models.BooleanField(default=False)

    def clean(self):
        """
        Validate the order before saving.
        Ensure that the ordered quantity does not exceed the available stock.
        """
        if self.quantity <= 0:
            raise ValidationError("Quantity must be at least 1.")

        if self.flower.available < self.quantity:
            raise ValidationError(
                f"Only {self.flower.available} units of '{self.flower.title}' are available."
            )

    def save(self, *args, **kwargs):
        """
        Override the save method to update the available stock of the flower.
        """
        # Validate before saving
        self.clean()

        # Reduce the available stock of the flower
        self.flower.available -= self.quantity
        self.flower.save()

        # Save the order
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Flower: {self.flower.title}, Buyer: {self.buyer.user.first_name}"
