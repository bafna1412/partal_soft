from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class User(models.Model):
    
    user = models.OneToOneField(User)


class Firm(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 100)
    address = models.TextField()
    contact_number = models.CharField(max_length = 11)
    PAN = models.CharField(max_length = 10, unique = True)
    TIN = models.CharField(max_length = 11, unique = True)
    net_commission = models.FloatField(default = 0.0)
    net_purchase_weight = models.FloatField(default = 0.0)
    net_purchase_amount = models.PositiveIntegerField(default = 0)


class Commodity(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 20)
    net_stock_raw = models.FloatField(default = 0.0)
    net_stock_processed = models.FloatField(default = 0.0)
    bags_raw = models.PositiveIntegerField(default = 0)
    bags_processed = models.PositiveIntegerField(default = 0)
    avg_price_raw = models.PositiveIntegerField(default = 0)
    avg_price_processed = models.PositiveIntegerField(default = 0)

class Product(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 20)
    commodity = models.ForeignKey(Commodity)
    net_stock_raw = models.FloatField(default = 0.0)
    net_stock_processed = models.FloatField(default = 0.0)
    bags_raw = models.PositiveIntegerField(default = 0)
    bags_processed = models.PositiveIntegerField(default = 0)
    avg_price_raw = models.PositiveIntegerField(default = 0)
    avg_price_processed = models.PositiveIntegerField(default = 0)
    
    def family(self):

        return self.commodity.name


class RateDetail(models.Model):

    commission = models.FloatField()
    mandi_tax = models.FloatField()
    association_charges = models.FloatField()
    dharmada = models.FloatField()
    muddat = models.FloatField()
    VAT = models.FloatField()
    TDS = models.FloatField()

    
class PurchaseInvoice(models.Model):
    
    date = models.DateField(default = datetime.date.today())
    seller = models.ForeignKey(Firm)
    seller_invoice_no = models.CharField(max_length = 10, default = "None")
    family = models.ForeignKey(Commodity)
    commission = models.FloatField()
    mandi_tax = models.FloatField()
    association_charges = models.FloatField()
    dharmada = models.FloatField()
    muddat = models.FloatField()
    VAT = models.FloatField()
    TDS = models.FloatField()
    amount = models.PositiveIntegerField()

    def merchant(self):

        return self.seller.name
    
    def commodity(self):
        
        return self.family.name


class PurchaseInvoiceDetail(models.Model):

    invoice = models.ForeignKey(PurchaseInvoice) 
    product = models.ForeignKey(Product)
    weight = models.FloatField(default = 0.0)
    bharti = models.PositiveIntegerField(max_length = 2, default = 0)
    rate = models.PositiveIntegerField(max_length = 5, default = 0)
    bags = models.PositiveIntegerField(default = 0)
    amount = models.FloatField()

    def invoice_no(self):

        return self.invoice.id

    def product_type(self):

        return self.product.name 

    def merchant(self):

        return self.invoice.seller.name


class DailyPurchase(models.Model):

    date = models.DateField(default = datetime.date.today())
    product = models.ForeignKey(Product)
    product_weight = models.FloatField(default = 0.0) 
    product_bags = models.PositiveIntegerField(default = 0)
    
    def product_name(self):

        return self.product.name 
 
