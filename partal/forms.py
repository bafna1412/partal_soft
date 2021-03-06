# Forms will be added here
from  django import forms
from django.forms import extras
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from partal.models import *
import datetime

PROCESS_CHOICES = (
    ('Sun Dry', 'Sun Dry'), ('Simple Clean', 'Simple Clean'),
    ('Semi Machine Clean', 'Semi Machine Clean'), ('Machine Clean', 'Machine Clean'),
    )

STORAGE_CHOICES = (
    ('Godown', 'Godown'), ('Cold', 'Cold')
    )

FIRM_CHOICES = (
    ('APB', 'APB'), ('KY', 'KY')
    )

TABLE_CHOICES = (
    ('invoice', 'Purchase Invoice'), ('detail', 'Purchase Detail'),
    ('process', 'Process Detail'), ('sale', 'Sale Invoice'),
    )


# Firm registration form
class FirmForm(forms.ModelForm):

    name = forms.CharField(help_text = "Firm Name", required = True, max_length = 100)
    group = forms.CharField(help_text = "Firm Group", max_length = 10, required = True) 
    address = forms.CharField(help_text = "Address of Firm", required = True, widget = forms.Textarea)
    contact_number = forms.CharField(help_text = "Contact Number", required = True, max_length = 11)
    PAN = forms.CharField(help_text = "PAN Number", max_length = 10)
    TIN = forms.CharField(help_text = "TIN Number", required = True, max_length = 11)
    net_commission_APB = forms.FloatField(help_text = "Net Commission APB",
                                          required = True, min_value = 0.0,
                                          initial = 0.0)
    net_commission_KY = forms.FloatField(help_text = "Net Commission KY",
                                          required = True, min_value = 0.0,
                                          initial = 0.0)
    
    class Meta:
        
        model = Firm
        fields = ('name', 'group', 'address', 'contact_number', 'PAN', 'TIN',
                  'net_commission_APB', 'net_commission_KY')


# Commodity registration form
class CommodityForm(forms.ModelForm):

    name = forms.CharField(help_text = "Commodity Name", required = True, max_length = 20)

    class Meta:
        
        model = Commodity
        fields = ('name',)


# Product registration form
class ProductForm(forms.ModelForm):

    name = forms.CharField(help_text = "Product Name", required = True, max_length = 20)
    
    family = forms.ModelChoiceField(help_text = "Commodity Type", required = True,
                                    queryset = Commodity.objects.values_list('name', flat=True), empty_label = None)
    
    class Meta:

        model = Product
        fields = ('name',)


# Purchase invoice entry form
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
                                 min_value = 0.0, initial = 0.0)

    weight = forms.FloatField(help_text = "Total Weight", required = True, min_value = 0.0,
                              widget=forms.TextInput(attrs={'readonly':'readonly'}))

    bags = forms.IntegerField(help_text = "Total Bags", required = True, min_value = 0,
                              widget=forms.TextInput(attrs={'readonly':'readonly'}))

    net_loose_amount = forms.FloatField(help_text = "Net Loose Amount", required = True,
                                        min_value = 0.0, widget=forms.TextInput(attrs={'readonly':'readonly'}))

    commission = forms.FloatField(help_text = "Commission", required = True, min_value = 0.0,
                                  widget=forms.TextInput(attrs={'readonly':'readonly'}))

    mandi_tax = forms.FloatField(help_text = "Mandi Tax", required = True, min_value = 0.0,
                                 widget=forms.TextInput(attrs={'readonly':'readonly'}))

    association_charges = forms.FloatField(help_text = "Association Charges", required = True,
                                           min_value = 0.0)

    dharmada = forms.FloatField(help_text = "Dharmada", required = True, min_value = 0.0)

    net_gross_amount = forms.FloatField(help_text = "Net Gross Amount", required = True,
                                        min_value = 0.0, widget=forms.TextInput(attrs={'readonly':'readonly'}))

    VAT = forms.FloatField(help_text = "VAT", required = True, min_value = 0.0,
                           widget=forms.TextInput(attrs={'readonly':'readonly'}))

    muddat = forms.FloatField(help_text = "Muddat", required = True, min_value = 0.0)

    TDS = forms.FloatField(help_text = "TDS", required = True, min_value = 0.0,
                           widget=forms.TextInput(attrs={'readonly':'readonly'}))

    amount = forms.FloatField(help_text = "Net Amount", required = True, min_value = 0.0,
                              widget=forms.TextInput(attrs={'readonly':'readonly'}))

    narration = forms.CharField(help_text = "Narration", required = False, widget = forms.Textarea)
    

    class Meta:

        model = PurchaseInvoice

        fields = ('date', 'seller', 'seller_invoice_no', 'family', 'firm', 'paid_with',  'weight',
                  'bags', 'net_loose_amount', 'commission', 'mandi_tax', 'association_charges',
                  'dharmada', 'VAT', 'muddat', 'TDS', 'amount', 'narration')



# Purchase detail entry form
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
    
    amount = forms.FloatField(help_text = "Amount (Rs.)", required = True, min_value = 0.0,
                              widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:

        model = PurchaseInvoiceDetail
        fields = ('date', 'seller', 'product', 'weight', 'bags', 'rate', 'amount')



# Purchase invoice date form
class DateForm(forms.Form):

    date = forms.DateField(help_text = "Purchase Invoice Date", initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)
    


# Sale estimate generation form
class SaleEstimateForm(forms.Form):

    start_date = forms.DateField(help_text = "From", initial = datetime.date.today, required = True,
                                 widget = SelectDateWidget)
    
    end_date = forms.DateField(help_text = "To", initial = datetime.date.today, required = True,
                                 widget = SelectDateWidget)
    
    product =  forms.ModelChoiceField(help_text = "Product", required = True,
                                      queryset = Product.objects.all(), empty_label = None)
    


# Sale invoice entry form
class SaleForm(forms.ModelForm):
    
    date = forms.DateField(help_text = "Invoice Date", initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)
    
    buyer = forms.ModelChoiceField(help_text = "Client Name", required = True,
                                    queryset = Client.objects.values_list('name', flat=True), empty_label = None)

    firm = forms.TypedChoiceField(help_text = "Billed Firm", required = True,
                                   choices = FIRM_CHOICES)
    
    invoice_no = forms.CharField(help_text = "Invoice No.", max_length = 10, required = True)

    family = forms.ModelChoiceField(help_text = "Commodity Type", required = True,
                                    queryset = Commodity.objects.all(),
                                    empty_label = None)
    
    storage = forms.TypedChoiceField(help_text = "Storage", required = True,
                                     choices = STORAGE_CHOICES)
    weight = forms.FloatField(help_text = "Total Weight", required = True,
                              min_value = 0.0, initial = 0.0,
                              widget=forms.TextInput(attrs={'readonly':'readonly'}))

    bags = forms.IntegerField(help_text = "Total Bags", required = True, min_value = 0,
                              initial = 0,
                              widget=forms.TextInput(attrs={'readonly':'readonly'}))

    net_loose_amount = forms.FloatField(help_text = "Net Loose Amount", required = True,
                                        min_value = 0.0, initial = 0.0,
                                        widget=forms.TextInput(attrs=
                                                               {'readonly':'readonly'}))

    VAT = forms.FloatField(help_text = "VAT", required = True, min_value = 0.0,
                           initial = 0.0,
                           widget=forms.TextInput(attrs={'readonly':'readonly'}))

    insurance = forms.FloatField(help_text = "Insurance", required = True,
                                 widget=forms.TextInput(attrs={'readonly':'readonly'}),
                                 initial = 0.0, min_value = 0.0)

    amount = forms.FloatField(help_text = "Net Amount", required = True, min_value = 0.0,
                              initial = 0.0,
                              widget=forms.TextInput(attrs={'readonly':'readonly'}))

    narration = forms.CharField(help_text = "Narration", required = False, widget = forms.Textarea)
    
    class Meta:

        model = SaleInvoice
        fields = ('date', 'buyer', 'firm', 'invoice_no', 'family', 'storage',
                  'weight', 'bags', 'net_loose_amount', 'VAT', 'insurance',
                  'amount', 'narration')



# Sale detail entry form
class SaleDetailForm(forms.ModelForm):

    product =  forms.ModelChoiceField(help_text = "Product", required = True,
                                      queryset = Product.objects.values_list(
                                          'name', flat=True), empty_label = None)
    product_weight = forms.FloatField(help_text = "Product Weight (Kg)",
                                      widget=forms.TextInput(
                                          attrs={'class':'per_weight'}),
                                      required = True, min_value = 0.0, initial = 0.0)
    product_bags = forms.IntegerField(help_text = "No. of bags", required = True,
                                      widget=forms.TextInput(attrs={'class':'per_bags'}),
                                      min_value = 0, initial = 0)
    product_rate = forms.IntegerField(help_text = "Product Rate (for Qtl)",
                                      widget=forms.TextInput(attrs={'class':'per_rate'}),
                                      required = True, min_value = 0, initial = 0)
    product_amount = forms.FloatField(help_text = "Amount", required = True,
                                      min_value = 0.0, initial = 0.0,
                                      widget=forms.TextInput(attrs={
                                          'readonly':'readonly',
                                          'class': 'per_amount'}))
    
    class Meta:

        model = SaleInvoiceDetail
        fields = ('product', 'product_weight', 'product_bags',
                  'product_rate', 'product_amount')



# Process entry form
class ProcessEntryForm(forms.ModelForm):

    date = forms.DateField(help_text = "Process Date", initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)
    product =  forms.ModelChoiceField(help_text = "Product", required = True,
                                      queryset = Product.objects.values_list('name', flat=True), empty_label = None)
    process = forms.TypedChoiceField(help_text = "Name of Process", required = True,
                                     choices = PROCESS_CHOICES)
    final_out = forms.BooleanField(help_text = "Dispatch Ready Product",
                                   required = False, initial = False)
    weight_in = forms.FloatField(help_text = "Raw Weight (Kg)", required = True, min_value = 0.0, initial = 0.0)
    bags_in = forms.IntegerField(help_text = "Raw Bags", required = True, min_value = 0,
                                 initial = 0)
    weight_out = forms.FloatField(help_text = "Processed Weight (Kg)", required = True, min_value = 0.0, initial = 0.0)
    bags_out = forms.IntegerField(help_text = "Processed Bags", required = True, min_value = 0, initial = 0)
    pulse_weight = forms.FloatField(help_text = "Pulse Weight (Kg)", required = True, min_value = 0.0, initial = 0.0)
    pulse_bags = forms.IntegerField(help_text = "Pulse Bags", required = True, min_value = 0, initial = 0)
    jhiri_weight = forms.FloatField(help_text = "Jhiri Weight (Kg)", required = True, min_value = 0.0, initial = 0.0)
    jhiri_bags = forms.IntegerField(help_text = "Jhiri Bags", required = True, min_value = 0, initial = 0)
    danthal_weight = forms.FloatField(help_text = "Danthal Weight (Kg)", required = True, min_value = 0.0, initial = 0.0)
    danthal_bags = forms.IntegerField(help_text = "Danthal Bags", required = True, min_value = 0, initial = 0)
    stone_weight = forms.FloatField(help_text = "Stone Weight (Kg)", required = True, min_value = 0.0, initial = 0.0)
    stone_bags = forms.IntegerField(help_text = "Stone Bags", required = True, min_value = 0, initial = 0)
    short_weight = forms.FloatField(help_text = "Weight Shortage (Kg)", required = True,
                                    initial = 0.0)
    percentage_out = forms.FloatField(help_text = "Percentage Output", required = True,
                                      min_value = 0.0, initial = 0.0,
                                      widget=forms.TextInput(attrs={'readonly':'readonly'
                                      }))
    storage = forms.TypedChoiceField(help_text = "Storage", required = True,
                                     choices = STORAGE_CHOICES)
    class Meta:
        
        model = ProcessEntry
        fields = ('date', 'product', 'process', 'final_out', 'weight_in', 'bags_in',
                  'weight_out', 'bags_out', 'pulse_weight', 'pulse_bags', 'jhiri_weight',
                  'jhiri_bags', 'danthal_weight', 'danthal_bags', 'stone_weight',
                  'stone_bags', 'short_weight', 'percentage_out', 'storage')



# TDS sheet generation form
class TdsViewForm(forms.Form):

    start_date = forms.DateField(help_text = "From", initial = datetime.date.today, required = True,
                                 widget = SelectDateWidget)
    
    end_date = forms.DateField(help_text = "To", initial = datetime.date.today, required = True,
                                 widget = SelectDateWidget)



# Super user functionalities form
class SuperUserForm(forms.Form):

    date = forms.DateField(help_text = "Date",
                           initial = datetime.date.today, required = True,
                           widget = SelectDateWidget)

    table = forms.TypedChoiceField(help_text = "Data Type", required = True,
                                    choices = TABLE_CHOICES)
    
    
