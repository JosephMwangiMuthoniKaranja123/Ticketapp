from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):

    name= models.CharField(max_length=100)
    description= models.TextField()
    category=models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    date=models.DateField()
    start_time=models.TimeField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):

    event=models.ForeignKey(Event, on_delete=models.CASCADE)
    status=models.CharField(max_length=50)
    ticket_type=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)

class TicketTypes(models.Model):
    event=models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_types")
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField()

class Cartitems(models.Model):
    user=models.ForeignKey(
        User,on_delete=models.CASCADE,related_name="cart_items"
    )
    ticketype=models.ForeignKey(TicketTypes,on_delete=models.CASCADE,related_name="cart_items")
    quantity=models.IntegerField(default=1)

    def totalprice(self):
        return self.ticketype.price * self.quantity

class Orders(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE, related_name="orders")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order_id=models.ForeignKey(Orders,on_delete=models.CASCADE)
    ticket_type=models.ForeignKey(TicketTypes,on_delete=models.PROTECT)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)

    


# Create your models here.
