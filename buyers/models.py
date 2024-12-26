from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.URLField(max_length=500, blank=True, null=True) 
    mobile_no = models.CharField(max_length = 12)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    class Meta:
        verbose_name_plural = "Buyers"