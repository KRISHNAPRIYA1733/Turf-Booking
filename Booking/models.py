from django.db import models

# Create your models here.
class TurfDb(models.Model):
    turf_name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    sport_type=models.CharField(max_length=100)
    price_per_hour=models.IntegerField()
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return self.turf_name

class BookingDb(models.Model):
    turf=models.ForeignKey(TurfDb,on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=100)
    booking_date=models.DateField()
    time_slot=models.TimeField()
    token_number=models.PositiveIntegerField(editable=False,null=True)
    total_price=models.IntegerField(editable=False,null=True)
    status=models.CharField(max_length=100,default="Pending")

    def __str__(self):
        return self.customer_name