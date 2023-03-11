from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from django_countries.fields import CountryField
from datetime import timedelta, datetime, date

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200, null=True, blank=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return str(self.pk)+'---'+str(self.user)+'---'+str(self.fullname)+'----'+str(self.phone)

class ShipmentAddress(models.Model):
    cust = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=50, blank=False, null=False)
    address_2 = models.CharField(max_length=50, blank=True)
    zip_code = models.PositiveIntegerField(blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    country = CountryField(blank=False)

    def __str__(self):
        return str(self.pk)+'---'+str(self.address_1)+'---'+str(self.address_2)+'---'+str(self.zip_code)+'---'+\
               str(self.city)+'---'+str(self.country)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.id)+'----'+str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    brand = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency = 'MAD')
    countInStock = models.PositiveIntegerField(null=True, blank=True, default=0)
    nbr_purchase = models.PositiveIntegerField(default=0)
    image = models.ImageField(null=True, blank=True)
    id_cat = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)+'---'+str(self.name)+'---'+str(self.brand)+'---'+str(self.description)+'---' +\
               str(self.price)+'---'+str(self.brand)+'---'+str(self.countInStock)+'---'+str(self.image)+'---'+\
               str(self.id_cat)

class Pictures(models.Model):
    image = models.ImageField(null=True, blank=True)
    id_prod = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)+'---'+str(self.id_prod)+'---'+str(self.image)

class Cart(models.Model):
    id_cust = models.OneToOneField(Customer, on_delete=models.CASCADE)
    GlobalPrice = MoneyField(max_digits=14, decimal_places=2, default_currency='MAD')

    def __str__(self):
        return str(self.pk)+'----'+str(self.GlobalPrice)+'----'+str(self.id_cust)


class Order(models.Model):
    id_cust = models.ForeignKey(Customer,on_delete=models.CASCADE, related_name='orders', null=False, blank=False)
    TotalPrice = MoneyField(max_digits=14, decimal_places=2, default_currency='MAD', default=0)
    delivered = models.BooleanField(default=False)
    date = models.DateField(default=date.today())
    time = models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    DeliveryDate = models.DateField(default=(datetime.today() + timedelta(days=4)))

    def __str__(self):
        return str(self.pk)+'--'+str(self.id_cust)+'--'+'--'+str(self.TotalPrice)+'--'+str(self.delivered)+'--' +\
               str(self.date)+'--'+str(self.time)


class ProductCart(models.Model):
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    id_prod=models.ForeignKey(Product, on_delete=models.CASCADE)
    id_order=models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    QuantityProd = models.PositiveIntegerField(default=0)
    TotalPrice = MoneyField(max_digits=14, decimal_places=2, default_currency='MAD')
    is_order = models.BooleanField(default=False)

    def __str__(self):
        return 'pk  '+str(self.pk)+'--quantityprod--'+str(self.QuantityProd) +\
               '-totalprice-'+str(self.TotalPrice)+'--id cart--'+str(self.id_cart)+'--id prod--'+str(self.id_prod) +\
               '--is_order--'+str(self.is_order)

"""class ProductOrder(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    QuantityProd = models.PositiveIntegerField(default=0)
    TotalPrice = MoneyField(max_digits=14, decimal_places=2, default_currency = 'MAD')

    def __str__(self):
        return str(self.pk)+'----'+str(self.QuantityProd) +\
               '---'+str(self.TotalPrice)+'----'+str(self.id_order)+'----'+str(self.id_prod)"""