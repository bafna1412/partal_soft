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
                       url(r'^purchase/$', views.purchase_invoice, name = 'purchase'),
                       )



