from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class User(models.Model):
    
    user = models.OneToOneField(User)

class Firm(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 100)
    address = models.TextField()
    contact_number = models.CharField(max_length = 10)
    PAN = models.CharField(max_length = 10, unique = True)
    TIN = models.CharField(max_length = 11, unique = True)
    net_commission = models.PositiveIntegerField(default = 0)
    net_purchase_weight = models.PositiveIntegerField(default = 0)
    net_purchase_amount = models.PositiveIntegerField(default = 0)

class Commodity(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 20)
    net_stock_raw = models.PositiveIntegerField(default = 0)
    net_stock_processed = models.PositiveIntegerField(default = 0)
    bags_raw = models.PositiveIntegerField(default = 0)
    bags_processed = models.PositiveIntegerField(default = 0)
    date = models.DateField(default = datetime.date.today())
    daily_purchase = models.PositiveIntegerField(default = 0)
    total_purchase = models.PositiveIntegerField(default = 0)

class Product(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 20)
    commodity = models.ForeignKey(Commodity)
    net_stock_raw = models.PositiveIntegerField(default = 0)
    net_stock_processed = models.PositiveIntegerField(default = 0)
    bags_raw = models.PositiveIntegerField(default = 0)
    bags_processed = models.PositiveIntegerField(default = 0)
    date = models.DateField(default = datetime.date.today())
    daily_purchase = models.PositiveIntegerField(default = 0)
    total_purchase = models.PositiveIntegerField(default = 0)

    def family(self):

        return self.commodity.name

class RateDetail(models.Model):

    commission = models.DecimalField(max_digits = 3, decimal_places = 2)
    mandi_tax = models.DecimalField(max_digits = 3, decimal_places = 2)
    association_charges = models.DecimalField(max_digits = 3, decimal_places = 2)
    dharmada = models.DecimalField(max_digits = 3, decimal_places = 2)
    muddat = models.DecimalField(max_digits = 3, decimal_places = 2)
    VAT = models.DecimalField(max_digits = 4, decimal_places = 2)
    TDS = models.DecimalField(max_digits = 4, decimal_places = 2)
    
class PurchaseInvoice(models.Model):
    
    date = models.DateField(default = datetime.date.today())
    seller = models.ForeignKey(Firm)
    seller_invoice_no = models.CharField(max_length = 10, default = "None")
    commission = models.DecimalField(max_digits = 8, decimal_places = 2)
    mandi_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    association_charges = models.DecimalField(max_digits = 7, decimal_places = 2)
    dharmada = models.DecimalField(max_digits = 7, decimal_places = 2)
    muddat = models.DecimalField(max_digits = 8, decimal_places = 2)
    VAT = models.DecimalField(max_digits = 8, decimal_places = 2)
    TDS = models.DecimalField(max_digits = 8, decimal_places = 2)
    amount = models.PositiveIntegerField()

    def merchant(self):

        return self.seller.name

    def product_type(self):

        return self.product.name 

class PurchaseDetail(models.Model):

    invoice = models.ForeignKey(PurchaseInvoice)
    product = models.ForeignKey(Product)
    weight = models.PositiveIntegerField()
    bharti = models.PositiveIntegerField(max_length = 2)
    rate = models.PositiveIntegerField(max_length = 5)
    bags = models.PositiveIntegerField()
