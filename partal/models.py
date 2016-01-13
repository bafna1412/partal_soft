from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class User(models.Model):
    
    user = models.OneToOneField(User)


class Firm(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 100)
    group = models.CharField(max_length = 10, default = "None")
    address = models.TextField()
    contact_number = models.CharField(max_length = 11)
    PAN = models.CharField(max_length = 10)
    TIN = models.CharField(max_length = 11, unique = True)
    net_commission_APB = models.FloatField(default = 0.0)
    net_commission_KY = models.FloatField(default = 0.0)
    net_purchase_weight = models.FloatField(default = 0.0)
    net_purchase_amount = models.PositiveIntegerField(default = 0)
    monthly_TDS_APB = models.FloatField(default = 0.0)
    monthly_TDS_KY = models.FloatField(default = 0.0)

    def __unicode__(self):
        
        return u'{0}'.format(self.name)


class Client(models.Model):

    name = models.CharField(unique = True, primary_key = True, max_length = 100)
    address = models.TextField()
    contact_number = models.CharField(max_length = 11)
    PAN = models.CharField(max_length = 10)
    TIN = models.CharField(max_length = 11, unique = True)
    net_sale_weight = models.FloatField(default = 0.0)
    net_sale_amount = models.PositiveIntegerField(default = 0)
    
    def __unicode__(self):
        
        return u'{0}'.format(self.name)



class Commodity(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 20)
    net_stock_raw = models.FloatField(default = 0.0)
    net_stock_processed = models.FloatField(default = 0.0)
    bags_raw = models.PositiveIntegerField(default = 0)
    bags_processed = models.PositiveIntegerField(default = 0)
    stock_cold = models.FloatField(default = 0.0)
    bags_cold = models.PositiveIntegerField(default = 0)
    avg_price_raw = models.PositiveIntegerField(default = 0)
    avg_price_processed = models.PositiveIntegerField(default = 0)

    def __unicode__(self):
        
        return u'{0}'.format(self.name)



class Product(models.Model):
    
    name = models.CharField(unique = True, primary_key = True, max_length = 20)
    commodity = models.ForeignKey(Commodity)
    net_stock_raw = models.FloatField(default = 0.0)
    net_stock_processed = models.FloatField(default = 0.0)
    bags_raw = models.PositiveIntegerField(default = 0)
    bags_processed = models.PositiveIntegerField(default = 0)
    stock_cold = models.FloatField(default = 0.0)
    bags_cold = models.PositiveIntegerField(default = 0)
    avg_price_raw = models.PositiveIntegerField(default = 0)
    avg_price_processed = models.PositiveIntegerField(default = 0)
    
    def __unicode__(self):
        
        return u'{0}'.format(self.name)

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
    insurance = models.FloatField(default = 0.0)
    

class PurchaseInvoice(models.Model):
    
    date = models.DateField(default = datetime.date.today())
    seller = models.ForeignKey(Firm)
    seller_invoice_no = models.CharField(max_length = 10, default = "None")
    family = models.ForeignKey(Commodity)
    firm = models.CharField(max_length = 10, default = "None")
    paid_with = models.FloatField(default = 0.0)
    weight = models.FloatField(default = 0.0)
    bags = models.PositiveIntegerField(default = 0)
    net_loose_amount = models.FloatField(default = 0.0)
    commission = models.FloatField()
    mandi_tax = models.FloatField()
    association_charges = models.FloatField()
    dharmada = models.FloatField()
    muddat = models.FloatField()
    VAT = models.FloatField()
    TDS = models.FloatField()
    amount = models.PositiveIntegerField()
    narration = models.TextField(default = "None")

    def merchant(self):

        return self.seller.name
    
    def commodity(self):
        
        return self.family.name


class PurchaseInvoiceDetail(models.Model):


    date = models.DateField(default = datetime.date.today())
    seller = models.ForeignKey(Firm)
    product = models.ForeignKey(Product)
    weight = models.FloatField(default = 0.0)
    rate = models.PositiveIntegerField(max_length = 5, default = 0)
    bags = models.PositiveIntegerField(default = 0)
    amount = models.FloatField()


    def product_type(self):

        return self.product.name 

    def merchant(self):

        return self.seller.group


class DailyPurchase(models.Model):

    date = models.DateField(default = datetime.date.today())
    product = models.ForeignKey(Product)
    product_weight = models.FloatField(default = 0.0) 
    product_bags = models.PositiveIntegerField(default = 0)
    total_purchase_amount = models.FloatField(default = 0.0)
    rate = models.FloatField(default = 0.0)

    def product_name(self):

        return self.product.name 


class SaleInvoice(models.Model):

    date = models.DateField(default = datetime.date.today())
    buyer = models.ForeignKey(Client)
    invoice_no = models.CharField(max_length = 10, default = "None", unique = True)
    family = models.ForeignKey(Commodity)
    storage = models.CharField(max_length = 25, default = "None")
    weight = models.FloatField(default = 0.0)
    bags = models.PositiveIntegerField(default = 0)
    VAT = models.FloatField()
    insurance = models.FloatField()
    amount = models.PositiveIntegerField()

    def client(self):

        return self.buyer.name
    
    def commodity(self):
        
        return self.family.name


class SaleInvoiceDetail(models.Model):

    invoice = models.ForeignKey(SaleInvoice) 
    product = models.ForeignKey(Product)
    weight = models.FloatField(default = 0.0)
    rate = models.PositiveIntegerField(max_length = 5, default = 0)
    bags = models.PositiveIntegerField(default = 0)
    amount = models.FloatField()

    def invoice_no(self):

        return self.invoice.invoice_no

    def product_type(self):

        return self.product.name 

    def client(self):

        return self.invoice.buyer.name



class ProcessEntry(models.Model):

    date = models.DateField(default = datetime.date.today())
    product = models.ForeignKey(Product)
    process = models.CharField(max_length = 100, default = "None")
    weight_in = models.FloatField(default = 0.0)
    bags_in = models.PositiveIntegerField(default = 0)
    weight_out = models.FloatField(default = 0.0)
    bags_out = models.PositiveIntegerField(default = 0)
    storage = models.CharField(max_length = 25, default = "None")

    def product_type(self):

        return self.product.name
