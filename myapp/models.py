from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    is_for_rent = models.BooleanField(default=False)

    def __str__(self):
        return self.title
