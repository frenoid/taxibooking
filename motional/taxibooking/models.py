from django.db import models

# Create your models here.
class Customer(models.Model):
	id = models.AutoField(primary_key=True)
	position_x = models.IntegerField(default=0)
	position_y = models.IntegerField(default=0)
	destination_x = models.IntegerField(default=0)
	destination_y = models.IntegerField(default=0)

class Car(models.Model):
	id = models.AutoField(primary_key=True)
	position_x = models.IntegerField(default=0)
	position_y = models.IntegerField(default=0)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
	BOOKING_STATE_CHOICES = [
        ('FREE', 'Free'), # Available to pick up customer
        ('ALLO', 'Allocted'), # Has been booked by a customer and on the way to pick up customer
        ('INTR', 'In transit') # Sending the passenger to the destination
    ]
	booking_state = models.CharField(max_length=4,
        choices=BOOKING_STATE_CHOICES,
        default='FREE',
    )

class Time(models.Model):
	tick = models.IntegerField(default=0)
