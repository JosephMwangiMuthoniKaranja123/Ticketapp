from django.db import models
from django.contrib.auth.models import User

class Order (models.Model):

    buyer=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)

class Event(models.Model):

    name= models.CharField(max_length=100)
    description= models.TextField()
    location= models.CharField(max_length=100)
    date=models.DateField()
    start_time=models.TimeField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)



class Ticket(models.Model):

    event=models.ForeignKey(Event, on_delete=models.CASCADE)
    status=models.CharField(max_length=50)
    ticket_type=models.CharField(max_length=50)
    price=models.DecimalField(decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):

    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE)
    ticket_type=models.CharField(50)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)



# Create your models here.
