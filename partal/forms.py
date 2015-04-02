# Forms will be added here
from  django import forms
from django.forms import extras
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from partal.models import *
import datetime

firms = Firm.objects.all()
FIRM_CHOICES = ()
for firm in firms:
    FIRM_CHOICES = FIRM_CHOICES + ((firm.name, firm.name),)

commodities = Commodity.objects.all()
FAMILY_CHOICES = ()
for commodity in commodities:
    FAMILY_CHOICES = FAMILY_CHOICES + ((commodity.name, commodity.name),)

products = Product.objects.all()
PRODUCT_CHOICES = ()
for product in products:
    PRODUCT_CHOICES = PRODUCT_CHOICES + ((product.name, product.name),)

 
class FirmForm(forms.ModelForm):

    name = forms.CharField(help_text = "Firm Name", required = True, max_length = 100)
    address = forms.CharField(help_text = "Address of Firm", required = True, widget = forms.Textarea)
    contact_number = forms.CharField(help_text = "Contact Number", required = True)
    PAN = forms.CharField(help_text = "PAN Number", max_length = 10)
    TIN = forms.CharField(help_text = "TIN Number", required = True, max_length = 11)
    
    class Meta:
        
        model = Firm
        fields = ('name', 'address', 'contact_number', 'PAN', 'TIN')



class CommodityForm(forms.ModelForm):

    name = forms.CharField(help_text = "Commodity Name", required = True, max_length = 20)

    class Meta:
        
        model = Commodity
        fields = ('name',)


class ProductForm(forms.ModelForm):

    name = forms.CharField(help_text = "Product Name", required = True, max_length = 20)
    
    family = forms.ModelChoiceField(help_text = "Commodity Type", required = True,
                                    queryset = Commodity.objects.values_list('name', flat=True))

    class Meta:

        model = Product
        fields = ('name',)


class PurchaseForm(forms.ModelForm):

    date = forms.DateField(help_text = "Invoice Date", initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)
    
    seller = forms.ModelChoiceField(help_text = "Firm Name", required = True,
                                    queryset = Firm.objects.values_list('name', flat=True))
    seller_invoice_no = forms.CharField(help_text = "Seller Invoice No.", max_length = 10, required = True)

    family = forms.ModelChoiceField(help_text = "Commodity Type", required = True,
                                    queryset = Commodity.objects.values_list('name', flat=True))
    
    class Meta:

        model = PurchaseInvoice
        fields = ('date', 'seller', 'seller_invoice_no', 'family')


class PurchaseDetailForm(forms.ModelForm):

    product =  forms.ModelChoiceField(help_text = "Product", required = True,
                                      queryset = Product.objects.values_list('name', flat=True))
    weight = forms.FloatField(help_text = "Product Weight (Kg)", required = True, min_value = 0.0)
    bharti = forms.IntegerField(help_text = "Per Bag Bharti (Kg)", required = True, min_value = 0)
    rate = forms.IntegerField(help_text = "Product Rate (for Qtl)", required = True, min_value = 0)

    class Meta:

        model = PurchaseInvoiceDetail
        fields = ('product', 'weight', 'bharti', 'rate')
