from django.contrib import admin
from partal.models import *
from totalsum.admin import TotalsumAdmin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse

import csv
from django.contrib.admin.util import label_for_field


def export_as_csv(description = "Download selected rows as CSV file", header = True):
    
    def export_as_csv(modeladmin, request, queryset):
        
        opts = queryset.model._meta
        
        field_names = modeladmin.list_display
        if 'action_checkbox' in field_names:
            field_names.remove('action_checkbox')
            
        response = HttpResponse(mimetype='text/csv')

        # Download
        response['Content-Disposition'] = 'attachment;filename=%s.csv' % unicode(opts).replace('.', '_')
        
        # Csv writer
        writer = csv.writer(response)
        if header:
            headers = []
            for field_name in list(field_names):
                label = label_for_field(field_name, modeladmin.model, modeladmin)
                headers.append(label)
            writer.writerow(headers)

        for row in queryset:
            values = []
            for field in field_names:
                value = (getattr(row, field))
                if callable(value):
                    try:
                        value = value() or ''
                    except:
                        value = 'Error retrieving value'
                if value is None:
                    value = ''
                values.append(unicode(value).encode('utf-8'))
            writer.writerow(values)
                    
        return response

    export_as_csv.short_description = description

    return export_as_csv


# Register your models here.

class FirmAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'group', 'address', 'contact_number', 'PAN', 'TIN', 'net_commission_APB', 'net_commission_KY', 'net_purchase_weight', 'net_purchase_amount')
    actions = [export_as_csv('Export as CSV')]
    
class ClientAdmin(admin.ModelAdmin):

    list_display = ('name', 'address', 'contact_number', 'PAN', 'TIN', 'net_sale_weight', 'net_sale_amount')
    actions = [export_as_csv('Export as CSV')]
    
class CommodityAdmin(admin.ModelAdmin):

    list_display = ('name', 'net_stock_raw', 'bags_raw', 'net_stock_processed', 'bags_processed', 'stock_cold', 'bags_cold')
    actions = [export_as_csv('Export as CSV')]
    
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'family', 'net_stock_raw', 'bags_raw', 'net_stock_processed', 'bags_processed', 'stock_cold', 'bags_cold')
    actions = [export_as_csv('Export as CSV')]
    
class RateDetailAdmin(admin.ModelAdmin):

    list_display = ('commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS', 'insurance')
    actions = [export_as_csv('Export as CSV')]
    
class PurchaseInvoiceAdmin(TotalsumAdmin):

    list_display = ('date', 'merchant', 'seller_invoice_no', 'firm', 'commodity', 'paid_with', 'weight', 'bags', 'net_loose_amount', 'commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS', 'amount', 'narration')
    list_filter = ('date', 'firm', 'seller__name')
    search_fields = ['date']
    totalsum_list = ('weight', 'bags', 'net_loose_amount', 'commission', 'mandi_tax', 'association_charges', 'dharmada', 'muddat', 'VAT', 'TDS', 'amount')
    actions = [export_as_csv('Export as CSV')]
    
class PurchaseInvoiceDetailAdmin(TotalsumAdmin):

    list_display = ('date', 'product_type', 'merchant', 'weight', 'rate', 'bags', 'amount')
    list_filter = ('date', 'product__name', 'seller__name')
    search_fields = ['date']
    totalsum_list = ('weight', 'bags', 'amount')
    actions = [export_as_csv('Export as CSV')]
    
class DailyPurchaseAdmin(TotalsumAdmin):

    list_display = ('date', 'product_name', 'product_weight', 'product_bags', 'total_purchase_amount', 'rate')
    list_filter = ('date', 'product__name')
    search_fields = ['date']
    totalsum_list = ('product_weight', 'product_bags', 'total_purchase_amount')
    actions = [export_as_csv('Export as CSV')]
    
class SaleInvoiceAdmin(admin.ModelAdmin):

    list_display = ('date', 'client', 'invoice_no', 'commodity', 'weight', 'bags', 'VAT', 'insurance', 'amount')
    actions = [export_as_csv('Export as CSV')]
    
class SaleInvoiceDetailAdmin(admin.ModelAdmin):

    list_display = ('invoice_no', 'product_type', 'client', 'weight', 'rate', 'bags', 'amount')
    actions = [export_as_csv('Export as CSV')]
    
class ProcessEntryAdmin(admin.ModelAdmin):

    list_display = ('date', 'product_type', 'process', 'weight_in', 'bags_in', 'weight_out', 'bags_out', 'storage')
    actions = [export_as_csv('Export as CSV')]
    


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
