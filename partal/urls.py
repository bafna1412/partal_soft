# URLs will be listed here

from django.conf.urls import patterns, url, include
from partal import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name = 'index'),
                       url(r'^home/$', views.home, name = 'home'),
                       url(r'^logout/$', views.user_logout, name = 'logout'),
                       url(r'^firm/$', views.firm_register, name = 'firm'),
                       url(r'^commodity/$', views.add_commodity, name = 'commodity'),
                       url(r'^product/$', views.add_product, name = 'product'),
                       url(r'^purchase/$', views.purchase_detail, name = 'purchase'),
                       url(r'^delete_purchase/(?P<entry_id>[0-9]+)/$', views.purchase_delete, name = 'delete_purchase'),
                       url(r'^invoice/$', views.purchase_invoice, name = 'invoice'),
                       url(r'^saveinvoice/(?P<date>[0-9_-]+)/(?P<seller>[\w&  ]+)/$', views.invoice_save, name = 'saveinvoice'),
                       url(r'^estimatesale/$', views.sale_estimate, name = 'estimatesale'),
                       url(r'^viewtds/$', views.tds_view, name = 'viewtds'),
                       url(r'^superuser/(?P<table>[\w&  ]+)/(?P<action>[\w&  ]+)/(?P<entry_id>[0-9]+)/$', views.super_user, name = 'superuser'),
                       url(r'^outputpdf/$', views.output_pdf, name = 'outputpdf'),
                       url(r'^process/$', views.process_entry, name = 'process'),
                       url(r'^sale/$', views.sale_invoice, name = 'sale'),
                       )



