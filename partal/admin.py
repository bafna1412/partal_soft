from django.contrib import admin
from partal.models import *

# Register your models here.

class FirmAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'address', 'contact_number', 'PAN', 'TIN', 'net_commission', 'net_purchase_weight', 'net_purchase_amount')

class CommodityAdmin(admin.ModelAdmin):

    list_display = ('name', 'net_stock_raw', 'net_stock_processed', 'bags_raw', 'bags_processed', 'date', 'daily_purchase', 'total_purchase')

class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'family', 'net_stock_raw', 'net_stock_processed', 'bags_raw', 'bags_processed', 'date', 'daily_purchase', 'total_purchase')

class RateDetailAdmin(admin.ModelAdmin):

    list_display = ('commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS')

class PurchaseInvoiceAdmin(admin.ModelAdmin):

    list_display = ('date', 'merchant', 'seller_invoice_no', 'commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS', 'amount')
 
class PurchaseDetailAdmin(admin.ModelAdmin):

    list_display = ('invoice', 'product', 'weight', 'bharti', 'rate', 'bags')

admin.site.register(Firm, FirmAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RateDetail, RateDetailAdmin)
admin.site.register(PurchaseInvoice, PurchaseInvoiceAdmin)
admin.site.register(PurchaseDetail, PurchaseDetailAdmin)
