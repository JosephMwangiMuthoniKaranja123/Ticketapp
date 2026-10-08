from django.contrib import admin
from .models import Order

class Orderadmin(admin.ModelAdmin):
  list_display= ("id","buyer","amount","status","created_at",)

admin.site.register(Order,Orderadmin)
# Register your models here.
