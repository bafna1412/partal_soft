from django.contrib import admin
from partal.models import *
from totalsum.admin import TotalsumAdmin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


# Register your models here.

class FirmAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'group', 'address', 'contact_number', 'PAN', 'TIN', 'net_commission_APB', 'net_commission_KY', 'net_purchase_weight', 'net_purchase_amount', 'monthly_TDS_APB', 'monthly_TDS_KY')

class ClientAdmin(admin.ModelAdmin):

    list_display = ('name', 'address', 'contact_number', 'PAN', 'TIN', 'net_sale_weight', 'net_sale_amount')

class CommodityAdmin(admin.ModelAdmin):

    list_display = ('name', 'net_stock_raw', 'bags_raw', 'net_stock_processed', 'bags_processed', 'stock_cold', 'bags_cold')

class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'family', 'net_stock_raw', 'bags_raw', 'net_stock_processed', 'bags_processed', 'stock_cold', 'bags_cold')

class RateDetailAdmin(admin.ModelAdmin):

    list_display = ('commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS', 'insurance')

class PurchaseInvoiceAdmin(TotalsumAdmin):

    list_display = ('date', 'merchant', 'seller_invoice_no', 'firm', 'commodity', 'weight', 'bags', 'net_loose_amount', 'commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS', 'amount', 'narration')
    list_filter = ('date', 'firm', 'seller__name')
    search_fields = ['date']
    totalsum_list = ('weight', 'bags', 'net_loose_amount', 'commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS', 'amount')
 
class PurchaseInvoiceDetailAdmin(TotalsumAdmin):

    list_display = ('date', 'product_type', 'merchant', 'weight', 'rate', 'bags', 'amount')
    list_filter = ('date', 'product__name', 'seller__name')
    search_fields = ['date']
    totalsum_list = ('weight', 'bags', 'amount')

class DailyPurchaseAdmin(TotalsumAdmin):

    list_display = ('date', 'product_name', 'product_weight', 'product_bags', 'total_purchase_amount', 'rate')
    list_filter = ('date', 'product__name')
    search_fields = ['date']
    totalsum_list = ('product_weight', 'product_bags', 'total_purchase_amount')

class SaleInvoiceAdmin(admin.ModelAdmin):

    list_display = ('date', 'client', 'invoice_no', 'commodity', 'weight', 'bags', 'VAT', 'insurance', 'amount')

class SaleInvoiceDetailAdmin(admin.ModelAdmin):

    list_display = ('invoice_no', 'product_type', 'client', 'weight', 'rate', 'bags', 'amount')

class ProcessEntryAdmin(admin.ModelAdmin):

    list_display = ('date', 'product_type', 'process', 'weight_in', 'bags_in', 'weight_out', 'bags_out', 'storage')


admin.site.register(Firm, FirmAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RateDetail, RateDetailAdmin)
admin.site.register(PurchaseInvoice, PurchaseInvoiceAdmin)
admin.site.register(PurchaseInvoiceDetail, PurchaseInvoiceDetailAdmin)
admin.site.register(DailyPurchase, DailyPurchaseAdmin)
admin.site.register(SaleInvoice, SaleInvoiceAdmin)
admin.site.register(SaleInvoiceDetail, SaleInvoiceDetailAdmin)
admin.site.register(ProcessEntry, ProcessEntryAdmin)
