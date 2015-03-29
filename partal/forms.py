# Forms will be added here

from  django import forms
from django.forms import extras
from django.contrib.auth.models import User
from partal.models import *

commodities = Commodity.objects.all()
FAMILY_CHOICES = ()
for commodity in commodities:
    FAMILY_CHOICES = FAMILY_CHOICES + ((commodity.name, commodity.name),)
 
class FirmForm(forms.ModelForm):

    name = forms.CharField(help_text = "Firm Name", required = True, max_length = 100)
    address = forms.CharField(help_text = "Address of Firm", required = True, widget = forms.Textarea)
    contact_number = forms.CharField(help_text = "Contact Number", required = True)
    PAN = forms.CharField(help_text = "PAN Number", required = True, max_length = 10)
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
    family = forms.TypedChoiceField(help_text = "Commodity Type", required = True,
                                   choices = FAMILY_CHOICES)

    class Meta:

        model = Product
        fields = ('name',)
