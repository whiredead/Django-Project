from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register([Product, Category, Customer, Cart, ProductCart, Pictures, Order, ShipmentAddress,])
