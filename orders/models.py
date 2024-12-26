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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

ORDER_STATUS = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Completed', 'Completed'),
    ('Rejected', 'Rejected'),
]
ORDER_TYPES = [
    ('Online', 'Online'),
    ('Offline', 'Offline'),
]

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    delivery_address = models.TextField()
    mobile_no = models.CharField(max_length=11)
    order_date = models.DateTimeField(default=now, editable=False)
    delivery_date = models.DateField()
    order_types = models.CharField(choices=ORDER_TYPES, max_length=10, default='Online')
    order_status = models.CharField(choices=ORDER_STATUS, max_length=10, default="Pending")
    cancel = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    # Price and total price fields
    price = models.FloatField(editable=False, default=0.0)
    # Price per unit
    total_price = models.FloatField(editable=False, default=0.0)  # Temporary default value
  # Total price (price * quantity)

    # def clean(self):
    #     """
    #     Validate the order before saving.
    #     Ensure that the ordered quantity does not exceed the available stock.
    #     """
    #     if self.quantity <= 0:
    #         raise ValidationError("Quantity must be at least 1.")

    #     if self.flower.available < self.quantity:
    #         raise ValidationError(
    #             f"Only {self.flower.available} units of '{self.flower.title}' are available."
    #         )

    # def save(self, *args, **kwargs):
    #     """
    #     Override the save method to update the available stock of the flower.
    #     """
    #     # Validate before saving
    #     self.clean()

    #     # Reduce the available stock of the flower only if it's a new order or quantity changes
    #     if self.pk:
    #         # If the order is being updated, adjust stock based on the difference in quantity
    #         original_order = Order.objects.get(pk=self.pk)
    #         stock_adjustment = self.quantity - original_order.quantity
    #     else:
    #         # For new orders, subtract the full quantity
    #         stock_adjustment = self.quantity

    #     if stock_adjustment > 0 and self.flower.available < stock_adjustment:
    #         raise ValidationError(
    #             f"Insufficient stock. Only {self.flower.available} units available for '{self.flower.title}'."
    #         )

    #     # Update the flower stock
    #     self.flower.available -= stock_adjustment
    #     self.flower.save()

    #     # Save the order
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"Flower: {self.flower.title}, Buyer: {self.buyer.user.first_name}"
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

            self.price = self.flower.price

            # Calculate the total price
            self.total_price = self.price * self.quantity

            # Reduce the available stock of the flower
            self.flower.available -= self.quantity
            self.flower.save()

            is_new = self.pk is None  # Check if this is a new order
            previous_status = None
            if not is_new:
                previous_status = Order.objects.get(pk=self.pk).order_status

            # Save the order
            super().save(*args, **kwargs)

            if is_new or previous_status != self.order_status:
                email_subject = f"Your Order Status: {self.order_status}"
                email_body = render_to_string('admin_email.html', {
                    'user': self.buyer.user,
                    'order_id': self.id,
                    'status': self.order_status,
                })

                email = EmailMultiAlternatives(
                    email_subject,
                    '',
                    to=[self.buyer.user.email]
                )
                email.attach_alternative(email_body, "text/html")
                email.send()

    def delete(self, *args, **kwargs):
            """
            Override the delete method to restore the flower's available quantity.
            """
            # Restore the available quantity of the flower
            self.flower.available += self.quantity
            self.flower.save()

            # Proceed with the default delete behavior
            super().delete(*args, **kwargs)

    

    def __str__(self):
            return f"Flower: {self.flower.title}, Buyer: {self.buyer.user.first_name}"