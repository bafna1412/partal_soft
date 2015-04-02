from django.contrib import admin
from partal.models import *

# Register your models here.

class FirmAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'address', 'contact_number', 'PAN', 'TIN', 'net_commission', 'net_purchase_weight', 'net_purchase_amount')

class CommodityAdmin(admin.ModelAdmin):

    list_display = ('name', 'net_stock_raw', 'net_stock_processed', 'bags_raw', 'bags_processed')

class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'family', 'net_stock_raw', 'net_stock_processed', 'bags_raw', 'bags_processed')

class RateDetailAdmin(admin.ModelAdmin):

    list_display = ('commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS')

class PurchaseInvoiceAdmin(admin.ModelAdmin):

    list_display = ('id', 'date', 'merchant', 'seller_invoice_no', 'commodity', 'commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS', 'amount')
 
class PurchaseInvoiceDetailAdmin(admin.ModelAdmin):

    list_display = ('invoice_no', 'product_type', 'merchant', 'weight', 'bharti', 'rate', 'bags', 'amount')

class DailyPurchaseAdmin(admin.ModelAdmin):

    list_display = ('date', 'product_name', 'product_weight', 'product_bags')


admin.site.register(Firm, FirmAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RateDetail, RateDetailAdmin)
admin.site.register(PurchaseInvoice, PurchaseInvoiceAdmin)
admin.site.register(PurchaseInvoiceDetail, PurchaseInvoiceDetailAdmin)
admin.site.register(DailyPurchase, DailyPurchaseAdmin)
