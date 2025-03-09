from django.db import models

class Newsletter(models.Model):
    cusEmail = models.EmailField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  # New field

    def __str__(self):
        return self.cusEmail

    class Meta:
        verbose_name_plural = "newsletter"