from django.db import models

# Create your models here.
class MenuItem(models.Model): 
    title = models.CharField(max_length=255, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    inventory = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.title} : {str(self.price)}'

class Booking(models.Model): 
    name = models.CharField(max_length=100, blank=False)
    slot = models.PositiveIntegerField(blank=False, default=1)
    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)