# Forms will be added here
from  django import forms
from django.forms import extras
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from partal.models import *
import datetime

PROCESS_CHOICES = (
    ('Taati Chanai', 'Taati Chanai'), ('Machine Clean', 'Machine Clean'),
    ('Chanai & Machine Clean', 'Chanai & Machine Clean'), ('Dry', 'Dry'),
    )

STORAGE_CHOICES = (
    ('Godown', 'Godown'), ('Cold', 'Cold')
    )

FIRM_CHOICES = (
    ('APB', 'APB'), ('KY', 'KY')
    )

class FirmForm(forms.ModelForm):

    name = forms.CharField(help_text = "Firm Name", required = True, max_length = 100)
    group = forms.CharField(help_text = "Firm Group", required = True, max_length = 10)
    address = forms.CharField(help_text = "Address of Firm", required = True, widget = forms.Textarea)
    contact_number = forms.CharField(help_text = "Contact Number", required = True)
    PAN = forms.CharField(help_text = "PAN Number", max_length = 10)
    TIN = forms.CharField(help_text = "TIN Number", required = True, max_length = 11)
    
    class Meta:
        
        model = Firm
        fields = ('name', 'group', 'address', 'contact_number', 'PAN', 'TIN')



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
                                    queryset = Firm.objects.all(), empty_label = None)
    
    seller_invoice_no = forms.CharField(help_text = "Bill Invoice No.", required = True, max_length = 10)

    family = forms.ModelChoiceField(help_text = "Commodity Type", required = True,
                                    queryset = Commodity.objects.all(), empty_label = None)
    
    firm = forms.TypedChoiceField(help_text = "Billed Firm", required = True,
                                   choices = FIRM_CHOICES)
    
    paid_with = forms.FloatField(help_text = "Paid With", required = False,
                                 min_value = 0.0)

    weight = forms.FloatField(help_text = "Total Weight", required = True, min_value = 0.0)

    bags = forms.IntegerField(help_text = "Total Bags", required = True, min_value = 0)

    net_loose_amount = forms.FloatField(help_text = "Net Loose Amount", required = True,
                                        min_value = 0.0)

    commission = forms.FloatField(help_text = "Commission", required = True, min_value = 0.0)

    mandi_tax = forms.FloatField(help_text = "Mandi Tax", required = True, min_value = 0.0)

    association_charges = forms.FloatField(help_text = "Association Charges", required = True,
                                           min_value = 0.0)

    dharmada = forms.FloatField(help_text = "Dharmada", required = True, min_value = 0.0)

    net_gross_amount = forms.FloatField(help_text = "Net Gross Amount", required = True,
                                        min_value = 0.0)

    VAT = forms.FloatField(help_text = "VAT", required = True, min_value = 0.0)

    muddat = forms.FloatField(help_text = "Muddat", required = True, min_value = 0.0)

    TDS = forms.FloatField(help_text = "TDS", required = True, min_value = 0.0)

    amount = forms.FloatField(help_text = "Net Amount", required = True, min_value = 0.0)

    narration = forms.CharField(help_text = "Narration", required = False, widget = forms.Textarea)
    

    class Meta:

        model = PurchaseInvoice

        fields = ('date', 'seller', 'seller_invoice_no', 'family', 'firm', 'weight',
                  'bags', 'net_loose_amount', 'commission', 'mandi_tax', 'association_charges',
                  'dharmada', 'VAT', 'muddat', 'TDS', 'amount', 'narration')



class PurchaseDetailForm(forms.ModelForm):


    date = forms.DateField(help_text = "Purchase Date", initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)
    
    seller = forms.ModelChoiceField(help_text = "Firm Group", required = True,
                                    queryset = Firm.objects.values_list('group', flat=True).distinct(), empty_label = None)
    
    product =  forms.ModelChoiceField(help_text = "Product", required = True,
                                      queryset = Product.objects.all(), empty_label = None)
    
    weight = forms.FloatField(help_text = "Product Weight (Kg)", required = True, min_value = 0.0)
    
    bags = forms.IntegerField(help_text = "No. of Bags", required = True, min_value = 0)
    
    rate = forms.IntegerField(help_text = "Product Rate (for Qtl)", required = True, min_value = 0)
    
    amount = forms.FloatField(help_text = "Amount (Rs.)", required = True, min_value = 0.0)

    class Meta:

        model = PurchaseInvoiceDetail
        fields = ('date', 'seller', 'product', 'weight', 'bags', 'rate', 'amount')


class DateForm(forms.Form):

    date = forms.DateField(help_text = "Purchase Invoice Date", initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)
    


class SaleEstimateForm(forms.Form):

    start_date = forms.DateField(help_text = "From", initial = datetime.date.today, required = True,
                                 widget = SelectDateWidget)
    
    end_date = forms.DateField(help_text = "To", initial = datetime.date.today, required = True,
                                 widget = SelectDateWidget)
    
    product =  forms.ModelChoiceField(help_text = "Product", required = True,
                                      queryset = Product.objects.all(), empty_label = None)
    


class SaleForm(forms.ModelForm):
    
    date = forms.DateField(help_text = "Invoice Date", initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)
    
    buyer = forms.ModelChoiceField(help_text = "Client Name", required = True,
                                    queryset = Client.objects.values_list('name', flat=True))
    invoice_no = forms.CharField(help_text = "Invoice No.", max_length = 10, required = True)

    family = forms.ModelChoiceField(help_text = "Commodity Type", required = True,
                                    queryset = Commodity.objects.values_list('name', flat=True))
    storage = forms.TypedChoiceField(help_text = "Storage", required = True,
                                     choices = STORAGE_CHOICES)
    
    class Meta:

        model = SaleInvoice
        fields = ('date', 'buyer', 'invoice_no', 'family', 'storage')


class SaleDetailForm(forms.ModelForm):

    product =  forms.ModelChoiceField(help_text = "Product", required = True,
                                      queryset = Product.objects.values_list('name', flat=True))
    weight = forms.FloatField(help_text = "Product Weight (Kg)", required = True, min_value = 0.0)
    bags = forms.IntegerField(help_text = "No. of bags", required = True, min_value = 0)
    rate = forms.IntegerField(help_text = "Product Rate (for Qtl)", required = True, min_value = 0)
    
    class Meta:

        model = SaleInvoiceDetail
        fields = ('product', 'weight', 'bags', 'rate')

    


class ProcessEntryForm(forms.ModelForm):

    date = forms.DateField(help_text = "Invoice Date", initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)
    product =  forms.ModelChoiceField(help_text = "Product", required = True,
                                      queryset = Product.objects.values_list('name', flat=True))
    process = forms.TypedChoiceField(help_text = "Name of Process", required = True,
                                     choices = PROCESS_CHOICES)
    weight_in = forms.FloatField(help_text = "Raw Weight (Kg)", required = True, min_value = 0.0)
    bags_in = forms.IntegerField(help_text = "Raw Bags", required = True, min_value = 0)
    weight_out = forms.FloatField(help_text = "Processed Weight (Kg)", required = True, min_value = 0.0)
    bags_out = forms.IntegerField(help_text = "Processed Bags", required = True, min_value = 0)
    storage = forms.TypedChoiceField(help_text = "Storage", required = True,
                                     choices = STORAGE_CHOICES)
    class Meta:
        
        model = ProcessEntry
        fields = ('date', 'product', 'process', 'weight_in', 'bags_in', 'weight_out', 'bags_out')
