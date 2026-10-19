from django.contrib import admin
from .models import Event,Ticket,TicketTypes,Cartitems,Orders,OrderItem

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(TicketTypes)
admin.site.register(Cartitems)
admin.site.register(Orders)
admin.site.register(OrderItem)

# Register your models here.
