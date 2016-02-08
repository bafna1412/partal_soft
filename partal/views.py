from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime

import json
from django.core.serializers.json import DjangoJSONEncoder

from partal.models import *
from partal.forms import *

from django.db.models import Sum, Q

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import *
from reportlab.lib.pagesizes import *
from reportlab.platypus import *
from reportlab.lib.enums import *

#from reportlab.platypus.tables import Table

# Create your views here.


# Login for Partal Entry
def index(request):
    context_dict = {}

    #Getting Login details
    if request.method == "POST":
        print "post"
        username = request.POST['username']
        password = request.POST['password']

        #Authenticating User
        user = authenticate(username = username, password = password)
        
        #Logging in the user
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/partal/home/')
            
            else:
                return HttpResponse("Your account is Disabled")
        
        else:
            print "Invalid Login detalils: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render(request, 'partal/index.html', context_dict)

    else:
        #Redirecting already logged in user
        if request.user.is_authenticated():
            return HttpResponseRedirect('/partal/home/')
        #If user is not logged in
        else:
            return render(request, 'partal/index.html', context_dict)


# Home Page
@login_required
def home(request):

    context_dict = {}
    return render(request, 'partal/home.html', context_dict)


# Logout
@login_required
def user_logout(request):

    # Logging out the user
    logout(request)

    # Take him to homepage
    return HttpResponseRedirect('/partal/')


# Firm Registration
@login_required
def firm_register(request):

    context_dict = {}
    firm_form = FirmForm()
    firm_groups = Firm.objects.values_list('group', flat=True).distinct()

    if request.method == "POST":

        # Grab the data
        firm_form = FirmForm(data = request.POST)

        # Check if data is valid
        if firm_form.is_valid():

            try:
                # Check if firm is already registered
                Firm.objects.get(name = request.POST['name'])

            except Firm.DoesNotExist:
                # Save firm data
                firm = firm_form.save()
                firm_form = FirmForm()
                context_dict = {"message": "Firm Registered",
                                "firm_form": firm_form,
                                "firm_groups": firm_groups
                                }

                return render(request, 'partal/firm.html', context_dict)

            else:
                # Already Registered
                context_dict = {"message": "Firm Already Registered"}
                return render(request, 'partal/firm.html', context_dict)

        else:
            # Errors in Form
            context_dict = {"firm_form": firm_form}
            return render(request, 'partal/firm.html', context_dict)

    else:
        # Not a POST Request
        context_dict = {"firm_form": firm_form,
                        "firm_groups": firm_groups
                        }
        
        return render(request, 'partal/firm.html', context_dict)


# Add Commodity
@login_required
def add_commodity(request):

    context_dict = {}
    commodity_form = CommodityForm()

    if request.method == "POST":

        # Grab the data
        commodity_form = CommodityForm(data = request.POST)

        # Check if data is valid
        if commodity_form.is_valid():

            try:
                # Check if commodity already exists
                Commodity.objects.get(name = request.POST['name'])

            except Commodity.DoesNotExist:
                # Add Commodity
                commodity = commodity_form.save()
                commodity_form = CommodityForm()
                context_dict = {"message": "Commodity Added",
                                "commodity_form": commodity_form}
    
                return render(request, 'partal/commodity.html', context_dict)

            else:
                # Already Present
                context_dict = {"message": "Commodity Already Present"}
                return render(request, 'partal/commodity.html', context_dict)

        else:
            # Errors in Form
            context_dict = {"commodity_form": commodity_form}
            return render(request, 'partal/commodity.html', context_dict)

    else:
        # Not a POST Request
        context_dict = {"commodity_form": commodity_form}
        return render(request, 'partal/commodity.html', context_dict)


# Add Product
@login_required
def add_product(request):

    context_dict = {}
    product_form = ProductForm()

    if request.method == "POST":

        # Grab the data
        product_form = ProductForm(data = request.POST)

        # Check if data is valid
        if product_form.is_valid():

            try:
                # Check if product already exists
                Product.objects.get(name = request.POST['name'])

            except Product.DoesNotExist:
                # Add Product
                family = Commodity.objects.get(name = request.POST['family'])
                new = Product(name = request.POST['name'], commodity = family)
                new.save()

                product_form = ProductForm()
                context_dict = {"message": "Product Added",
                                "product_form": product_form}
                
                return render(request, 'partal/product.html', context_dict)

            else:
                # Already Present
                context_dict = {"message": "Product Already Present"}
                return render(request, 'partal/product.html', context_dict)

        else:
            # Errors in Form
            context_dict = {"product_form": product_form}
            return render(request, 'partal/product.html', context_dict)

    else:
        # Not a POST Request
        context_dict = {"product_form": product_form}
        return render(request, 'partal/product.html', context_dict)



# Purchase Detail Entry
@login_required
def purchase_detail(request):

    purchase_detail_form = PurchaseDetailForm()
    #Showing earlier entry data for the same date
    history = PurchaseInvoiceDetail.objects.filter(date = datetime.date.today())
    bags_total = history.aggregate(Sum('bags'))['bags__sum']
    weight_total = history.aggregate(Sum('weight'))['weight__sum']
        
    context_dict = {"purchase_detail_form": purchase_detail_form,
                    "history": history,
                    "bags_total": bags_total,
                    "weight_total": weight_total,
                    }

    if request.method == 'POST':

        purchase_detail_form = PurchaseDetailForm(data = request.POST)

        #Errors in the form
        if not request.POST['weight'] or not request.POST['bags'] or not request.POST['rate'] or not request.POST['amount']:

            #Showing earlier entry data for the same date
            date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
            history = PurchaseInvoiceDetail.objects.filter(date = date)
            bags_total = history.aggregate(Sum('bags'))['bags__sum']
            weight_total = history.aggregate(Sum('weight'))['weight__sum']
        
            context_dict = {"purchase_detail_form": purchase_detail_form,
                            "history": history,
                            "bags_total": bags_total,
                            "weight_total": weight_total,
                            }
            
        else:

            #Getting all the data
            date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
            merchant = Firm.objects.filter(group = request.POST['seller'])
            product = Product.objects.get(name = request.POST['product'])
            weight = request.POST['weight']
            bags = request.POST['bags']
            rate = request.POST['rate']
            amount = request.POST['amount']
            rate_kg = float(rate)/100
        
            #Saving Purchase Detail
            purchase_invoice_detail = PurchaseInvoiceDetail(date = date,
                                                            seller = merchant[0],
                                                            product = product,
                                                            weight = weight,
                                                            rate = rate,
                                                            bags = bags,
                                                            amount = amount
                                                            )
            purchase_invoice_detail.save()
        
            #Updating Daily Purchase
            entries = DailyPurchase.objects.filter(date = date)
        
            #If no entry is found for the given date
            if not entries:
                entry = DailyPurchase(date = date,
                                      product = product,
                                      product_weight = weight,
                                      product_bags = bags,
                                      total_purchase_amount = amount,
                                      rate = rate_kg
                                      )
            
                entry.save()

            #If some entry is present
            else:
                #Check if entry for particular product is present
                try:
                    entry = DailyPurchase.objects.get(date = date, product = product)
                
                except DailyPurchase.DoesNotExist:
                
                    entry = DailyPurchase(date = date,
                                          product = product,
                                          product_weight = weight,
                                          product_bags = bags,
                                          total_purchase_amount = amount,
                                          rate = rate_kg
                                          )
                    entry.save()
                
                else:
                    entry.product_weight += float(weight)
                    entry.product_bags += int(bags)
                    entry.total_purchase_amount += float(amount)
                    entry.rate = entry.total_purchase_amount/entry.product_weight
                    
                    entry.save()
      
            #Updating Commodity quanity
            commodity = Commodity.objects.get(name = product.commodity.name)
            commodity.net_stock_raw += float(weight)
            commodity.bags_raw += int(bags)
            commodity.save()
          
            #Updating Product quanity
            product.net_stock_raw += float(weight)
            product.bags_raw += int(bags)
            product.save()
          
            #Setting the entry date for further entries
            purchase_detail_form = PurchaseDetailForm(initial = {'date': date},)
            #Showing earlier entry data for the same date
            history = PurchaseInvoiceDetail.objects.filter(date = date)
            bags_total = history.aggregate(Sum('bags'))['bags__sum']
            weight_total = history.aggregate(Sum('weight'))['weight__sum']
        
            context_dict = {"purchase_detail_form": purchase_detail_form,
                            "history": history,
                            "bags_total": bags_total,
                            "weight_total": weight_total,
                            }
            
        return render(request, 'partal/purchase.html', context_dict)

    else:
        #Not a post request
        #context_dict = {"purchase_detail_form": purchase_detail_form}

        return render(request, 'partal/purchase.html', context_dict)


    
# Function to delete purchase detail entry
def delete_purchase_detail(entry):

    #Make changes to daily purchase
    daily_purchase = DailyPurchase.objects.get(date = entry.date,
                                               product = entry.product)

    daily_purchase.product_weight -= float(entry.weight)
    daily_purchase.product_bags -= int(entry.bags)
    daily_purchase.total_purchase_amount -= float(entry.amount)
    if daily_purchase.product_weight == 0.0:
        daily_purchase.rate = 0.0 
    else:
        daily_purchase.rate = daily_purchase.total_purchase_amount/daily_purchase.product_weight
        
    daily_purchase.save()

    #Make changes to Product quantity
    product = Product.objects.get(name = entry.product)

    product.net_stock_raw -= float(entry.weight)
    product.bags_raw -= int(entry.bags)
    
    product.save()
    
    #Make changes to Commodity quantity
    commodity = Commodity.objects.get(name = product.commodity.name)
    
    commodity.net_stock_raw -= float(entry.weight)
    commodity.bags_raw -= int(entry.bags)
    
    commodity.save()
    
    #Delete the purchase detail entry
    entry.delete()

        

# Delete Purchase detail
@login_required
def purchase_delete(request, entry_id):

    #Fetch the entry to be deleted
    entry = PurchaseInvoiceDetail.objects.get(id = entry_id)
    firms = Firm.objects.filter(group = entry.seller.group)
    entries = []

    # Check if entry is billed. Billed entries can't be deleted.
    for firm in firms:
        
        invoices = PurchaseInvoice.objects.filter(date = entry.date, seller = firm.name)
        if invoices:
            entries.append(invoices)

    # Make changes only if invoice is not made
    if not entries:
        
        delete_purchase_detail(entry)
        
    return HttpResponseRedirect('/partal/purchase/')
          


# Purhcase Invoice generation and entry
@login_required
def purchase_invoice(request):

    context_dict = {}
    date_form = DateForm()

    if request.method == 'POST':

        date_form = DateForm(data = request.POST)

        if date_form.is_valid():

            date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
            date_form = DateForm(initial = {'date': date},)

            #Fetching name of all the merchants from purchase details for this date
            entries = PurchaseInvoiceDetail.objects.filter(date = date)

            if not entries:
                
                context_dict = {"date": date,
                                "date_form": date_form
                                }

            else:
                sellers = entries.values_list('seller', flat = True).distinct()
                count = len(sellers)
                context_dict = {"sellers": sellers,
                                "count": count,
                                "date": date,
                                "date_form": date_form
                                }
                
            return render(request, 'partal/invoice.html', context_dict)
        
        else:
            
            # Errors in Form
            context_dict = {"date_form": date_form}
            return render(request, 'partal/invoice.html', context_dict)
        
    else:
        #Not a post request
        context_dict = {"date_form": date_form}

        return render(request, 'partal/invoice.html', context_dict)



# Saving Purchase Invoice
@login_required
def invoice_save(request, date, seller):

    context_dict = {}
    purchase_form = PurchaseForm()
    list = []

    #Retrieving list of prospective merchants
    merchant = Firm.objects.get(name = seller)
    purchase_form = PurchaseForm(initial = {'date': date,})
    sellers = Firm.objects.filter(group = merchant.group)

    #Making the query set for the form
    purchase_form.fields['seller'].queryset = sellers
    
    #Entries of the seller selected
    entries = PurchaseInvoiceDetail.objects.filter(seller = seller, date = date)
    
    #Getting all the extra charge rates
    charges = RateDetail.objects.get(id = 1)

    #Making seller commission list
    for seller_name in sellers:
        list.append({"name": seller_name.name, "APB": seller_name.net_commission_APB, "KY": seller_name.net_commission_KY})

    list_json = json.dumps(list, cls=DjangoJSONEncoder)


    if request.method == "POST":

        purchase_form = PurchaseForm(data = request.POST)

        #Check validity of data
        if purchase_form.is_valid():

            try:
                
                #Check if entry already present
                entry = PurchaseInvoice.objects.get(date = date, seller = request.POST['seller'], paid_with = request.POST['paid_with'])
                
            except PurchaseInvoice.DoesNotExist:
                
                #If no duplicate entry. Saving the entry
                purchase = purchase_form.save()

                #Updating Firm Record
                firm = Firm.objects.get(name = request.POST['seller'])

                firm.net_purchase_weight += float(request.POST['weight'])
                firm.net_purchase_amount += int(request.POST['amount'])

                if request.POST['firm'] == "APB":
                    firm.net_commission_APB += float(request.POST['commission'])
                if request.POST['firm'] == "KY":
                    firm.net_commission_KY += float(request.POST['commission'])
                
                firm.save()
                return HttpResponse('<script type="text/javascript">window.close()</script>')
                #context_dict = {"message": "Purchase Invoice Saved"}
            
            else:
                #Duplicate entry exists

                #Making the query set for the form
                purchase_form.fields['seller'].queryset = sellers
    
                context_dict = {"message": "Entry for this Seller for this date already exists.",
                                "message1": "If you wish to rewrite this entry then please delete the old record first.",
                                "date": date,
                                "seller": seller,
                                "purchase_form": purchase_form,
                                "entries": entries,
                                "list": list_json,
                                "charges": charges,
                                }

        # Errors in Form
        else:

            #Making the query set for the form
            purchase_form.fields['seller'].queryset = sellers
    
            #Return errors
            context_dict = {"date": date,
                            "seller": seller,
                            "purchase_form": purchase_form,
                            "entries": entries,
                            "list": list_json,
                            "charges": charges,
                            }
            print entries


                
        return render(request, 'partal/saveinvoice.html', context_dict)


    else:

        context_dict = {"date": date,
                        "seller": seller,
                        "purchase_form": purchase_form,
                        "entries": entries,
                        "list": list_json,
                        "charges": charges,
                        }
        
        return render(request, 'partal/saveinvoice.html', context_dict)


    
# Sale Estimate
@login_required
def sale_estimate(request):

    context_dict = {}
    sale_estimate_form = SaleEstimateForm()

    if request.method == "POST":
        
        sale_estimate_form = SaleEstimateForm(data = request.POST)

        if sale_estimate_form.is_valid():

            start_date = request.POST['start_date_year'] + "-" + request.POST['start_date_month'] + "-" + request.POST['start_date_day']
            end_date = request.POST['end_date_year'] + "-" + request.POST['end_date_month'] + "-" + request.POST['end_date_day']
            
            data = PurchaseInvoiceDetail.objects.filter(date__gte = start_date, date__lte = end_date, product = request.POST['product'])

            context_dict = {"sale_estimate_form": sale_estimate_form,
                            "data": data,
                            }

        else:
            # Errors in form
            context_dict = {"sale_estimate_form": sale_estimate_form}

    else:
            # Not a post request
            context_dict = {"sale_estimate_form": sale_estimate_form}

    return render(request, 'partal/estimatesale.html', context_dict)



# TDS view for all the firms
@login_required
def tds_view(request):
    
    context_dict = {}
    tds_view_form = TdsViewForm()
    data = []

    if request.method == 'POST':

        tds_view_form = TdsViewForm(data = request.POST)

        if tds_view_form.is_valid():

            start_date = request.POST['start_date_year'] + "-" + request.POST['start_date_month'] + "-" + request.POST['start_date_day']
            end_date = request.POST['end_date_year'] + "-" + request.POST['end_date_month'] + "-" + request.POST['end_date_day']

            firms = Firm.objects.all()

            # Fetching and Aggregating data for each firm
            for firm in firms:

                entries = PurchaseInvoice.objects.filter(date__gte = start_date,
                                                         date__lte = end_date,
                                                         seller = firm)

                # If entires for the firm are preset
                if entries:
                    
                    entries_APB = entries.filter(firm = 'APB')
                    count_entries_APB = len(entries_APB)

                    # If no entries in APB
                    if not entries_APB:
                        commission_APB = 0.0
                        tds_APB = 0.0
                    else:    
                        commission_APB = entries_APB.aggregate(
                            Sum('commission'))['commission__sum']
                        tds_APB = entries_APB.aggregate(Sum('TDS'))['TDS__sum']
                    
                    entries_KY = entries.filter(firm = 'KY')
                    count_entries_KY = len(entries_KY)

                    # If no entries in KY
                    if not entries_KY:
                        commission_KY = 0.0
                        tds_KY = 0.0
                    else:
                        commission_KY = entries_KY.aggregate(
                            Sum('commission'))['commission__sum']
                        tds_KY = entries_KY.aggregate(Sum('TDS'))['TDS__sum']

                    # Updating data array
                    data.append([firm.name, count_entries_APB, commission_APB, tds_APB,
                                 count_entries_KY, commission_KY, tds_KY])

                # If there are no entries for firm
                else:
                    data.append([firm.name, 0, 0.0, 0.0, 0, 0.0, 0.0])

            # Calculating total values
            total_bills_APB = 0
            total_commission_APB = 0.0
            total_tds_APB = 0.0
            total_bills_KY = 0
            total_commission_KY = 0.0
            total_tds_KY = 0.0
            
            for values in data:
                total_bills_APB += values[1]
                total_commission_APB += values[2]
                total_tds_APB += values[3]
                total_bills_KY += values[4]
                total_commission_KY += values[5]
                total_tds_KY += values[6]

            context_dict = {"tds_view_form": tds_view_form,
                            "data": data,
                            "total_bills_APB": total_bills_APB,
                            "total_bills_KY": total_bills_KY,
                            "total_commission_APB": total_commission_APB,
                            "total_commission_KY": total_commission_KY,
                            "total_tds_APB": total_tds_APB,
                            "total_tds_KY": total_tds_KY,
                            }

        else:
            # Errors in form
            context_dict = {"tds_view_form": tds_view_form}

    else:
        # Not a post request
        context_dict = {"tds_view_form": tds_view_form}

    return render(request, 'partal/viewtds.html', context_dict)


            
# Super user functionalities
@user_passes_test(lambda u: u.is_superuser)
def super_user(request, table, action, entry_id):

    super_user_form = SuperUserForm()
    context_dict = {}

    if request.method == 'POST':

        super_user_form = SuperUserForm(data = request.POST)

        if super_user_form.is_valid():
            
            date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
        
            # Post request to view entries
            if (action == 'view'):

                # Fetch and send entries from Purchase Invoice table
                if (request.POST['table'] == 'invoice'):
                    data = PurchaseInvoice.objects.filter(date = date)

                # Fetch and send entries from Purchase Detail table
                if (request.POST['table'] == 'detail'):
                    data = PurchaseInvoiceDetail.objects.filter(date = date)

                # Fetch and send entries from Process Entry table
                if (request.POST['table'] == 'process'):
                    data = ProcessEntry.objects.filter(date = date)

                # Fetch and send entries from Sale Invoice table
                if (request.POST['table'] == 'sale'):
                    data = SaleInvoice.objects.filter(date = date)


                context_dict = {"data": data,
                                "table": request.POST['table'],
                                "super_user_form": super_user_form
                                }
        else:
            # Errors in form
            context_dict = {"super_user_form": super_user_form}

    else:
        # Request for delete
        if (action == "delete"):
            
            # Delete entry from Purchase Invoice table
            if (table == 'invoice'):
                
                entry = PurchaseInvoice.objects.get(id = entry_id)
                
                #Updating Firm Record
                firm = Firm.objects.get(name = entry.seller.name)
                
                firm.net_purchase_weight -= float(entry.weight)
                firm.net_purchase_amount -= int(entry.amount)
                
                if entry.firm == "APB":
                    firm.net_commission_APB -= float(entry.commission)
                if entry.firm == "KY":
                    firm.net_commission_KY -= float(entry.commission)
                
                firm.save()
                
                # Delete entry
                entry.delete()

                # Redirect to make new entry
                return HttpResponseRedirect('/partal/invoice/')

            # Delete entry from Purhcase Invoice Detail Table
            if (table == 'detail'):
                
                entry = PurchaseInvoiceDetail.objects.get(id = entry_id)
                
                # Make changes and delete entry
                delete_purchase_detail(entry)
                
                # Redirect to make new entry
                return HttpResponseRedirect('/partal/purchase/')

            if (table == 'process'):

                entry = ProcessEntry.objects.get(id = entry_id)

                # Updating Product and Commodity Records
                product = Product.objects.get(name = entry.product.name)
                commodity = Commodity.objects.get(name = entry.product.commodity.name)
                
                if entry.final_out:
                    
                    # Update final processed fields
                    if entry.storage == str('Godown'):
                        product.net_stock_processed -= entry.weight_out
                        product.bags_processed -= entry.bags_out

                        commodity.net_stock_processed -= entry.weight_out
                        commodity.bags_processed -= entry.bags_out
                        
                    else:
                        product.stock_cold -= entry.weight_out
                        product.bags_cold -= entry.bags_out

                        commodity.stock_cold -= entry.weight_out
                        commodity.bags_cold -= entry.bags_out
                        
                # Update raw fields
                else:
                    if product.net_stock_raw - entry.weight_out < 0 and product.bags_raw - entry.bags_out < 0:
                        context_dict = {'message': "First delete the final process entry for this product",
                                        'super_user_form': super_user_form,
                                        }
                        return render(request, 'partal/superuser.html', context_dict)
                
                    else:
                        
                        product.net_stock_raw -= entry.weight_out
                        product.bags_raw -= entry.bags_out

                        commodity.net_stock_raw -= entry.weight_out
                        commodity.bags_raw -= entry.bags_out 
                
                product.net_stock_raw += entry.weight_in
                product.bags_raw += entry.bags_in

                commodity.net_stock_raw += entry.weight_in
                commodity.bags_raw += entry.bags_in                
            
                product.save()
                commodity.save()

                # Update pulse details
                pulse_detial = Commodity.objects.get(name = 'Pulse')
                
                pulse_detial.net_stock_processed -= entry.pulse_weight
                pulse_detial.bags_processed -= entry.pulse_bags

                pulse_detial.save()
                
                # Update waste product details
                reduce_waste_detail('Jhiri', entry.jhiri_weight, entry.jhiri_bags)
                reduce_waste_detail('Danthal', entry.danthal_weight, entry.danthal_bags)
                reduce_waste_detail('Stone', entry.stone_weight, entry.stone_bags)

                entry.delete()
                
                # Redirect to make new entry
                return HttpResponseRedirect('/partal/process/')

            if (table == 'sale'):

                # Fetch sale invoice entry
                entry = SaleInvoice.objects.get(id = entry_id)
                # Fetch client entry
                client = Client.objects.get(name = entry.buyer.name)

                # Update client data
                client.net_sale_weight -= entry.weight
                client.net_sale_amount -= entry.amount
                client.save()

                # Update commodity data
                commodity = Commodity.objects.get(name = entry.family.name)
                if (entry.storage == 'Godown'):
                    commodity.net_stock_processed += entry.weight
                    commodity.bags_processed += entry.bags

                if (entry.storage == 'Cold'):
                    commodity.stock_cold += entry.weight
                    commodity.bags_cold += entry.bags

                commodity.save()

                # Update product data
                if (entry.family.name != 'Pulse'):
                    # Fetch sale invoice detail entries
                    sale_details = SaleInvoiceDetail.objects.filter(invoice = entry)
                    for detail in sale_details:
                        product = Product.objects.get(name = detail.product.name)
                        
                        if (entry.storage == 'Godown'):
                            product.net_stock_processed += detail.weight
                            product.bags_processed += detail.bags

                        if (entry.storage == 'Cold'):
                            product.stock_cold += detail.weight
                            product.bags_cold += detail.bags

                        product.save()

                entry.delete()

                # Redirect to make new entry
                return HttpResponseRedirect('/partal/sale/')


        # Not a post or delete request
        else:
            context_dict = {"super_user_form": super_user_form}
            


    return render(request, 'partal/superuser.html', context_dict)


    
# Print pdf option
@login_required
def output_pdf(request):

    dict = {}
        
    cm = 2.54
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name = 'RightAlign', alignment = TA_RIGHT))
    styles.add(ParagraphStyle(name = 'HeaderCenter', fontName='Times-Roman',
                              fontSize=20, alignment = TA_CENTER))
    styles.add(ParagraphStyle(name = 'CenterAlign', alignment = TA_CENTER))
    
    if request.method == 'POST':

        for key in request.POST:
            list = request.POST.getlist(key)
            dict.update({key: [val for val in list]})
        
        #Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{output}_{date}.pdf"'.format(output = dict['submit'][0], date = dict['date'][0])
        
        #Create the PDF object, using the response object as its "file."
        elements = []
        doc = SimpleDocTemplate(response, pagesize = A4, rightMargin = 0, leftMargin = 6.5 * cm,
                                topMargin = 0.3 * cm, bottomMargin = 0)
        
        #Draw things on the PDF. Here's where the PDF generation happens.
        elements.append(Paragraph("AGARCHAND POONAMCHAND BAFNA <br/> <br/>", styles['HeaderCenter']))
        elements.append(Paragraph(dict['submit'][0], styles['HeaderCenter']))
        elements.append(Paragraph("Date: " + request.POST['date'], styles['RightAlign']))
        elements.append(Paragraph("Name: " + str(request.POST['name']) + "<br/> <br/>", styles['Heading4']))
        
        elements.append(Paragraph("Quality: " + str(dict['quality'][0]), styles['Heading4']))

        #Table Styling
        tblStyle = TableStyle([('TEXTCOLOR', (0,0), (3,0), colors.white),
                               ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
                               ('VALIGN', (0,0), (-1,-1), 'TOP'),
                               ('LINEBELOW', (0,0), (-1,-1), 1, colors.black),
                               ('BOX', (0,0), (0,-1), 1, colors.black),
                               ('BOX', (1,0), (1,-1), 1, colors.black),
                               ('BOX', (2,0), (2,-1), 1, colors.black),
                               ('BOX', (0,0), (-1,-1), 1, colors.black)])
        tblStyle.add('BACKGROUND', (0,0), (4,0), colors.gray)
        tblStyle.add('BACKGROUND',(0,1), (-1,-1), colors.white)

        #Make heading for each column and start data list
        column1Heading = "Bags"
        column2Heading = "Weight(Kg)"
        column3Heading = "Rate(Rs)"
        column4Heading = "Amount(Rs)"

        #Assemble data for each column using simple loop to append it into data list
        data = [[column1Heading, column2Heading, column3Heading, column4Heading]]

        for i in range (0, len(dict['bags'])):
            data.append([dict['bags'][i], dict['weight'][i], dict['rate'][i], dict['amount'][i]])
        
        tableThatSplitsOverPages = Table(data, [25*cm, 25*cm, 25*cm, 25*cm], repeatRows=1)
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tableThatSplitsOverPages.setStyle(tblStyle)
        
        #Assemble Total Table 
        total_data = [[dict['bags_total'][0], dict['weight_total'][0], " ", dict['amount_total'][0]]]
        total_table = Table(total_data, [25*cm, 25*cm, 25*cm, 25*cm]) 
        total_table.setStyle(tblStyle)
        
        elements.append(tableThatSplitsOverPages)
        elements.append(total_table)

        #Close the PDF object cleanly
        doc.build(elements) 

        return response



# Sale Invoice
@login_required
def sale_invoice(request):

    context_dict = {}
    sale_form = SaleForm()
    sale_detail_form = SaleDetailForm()
    charges = RateDetail.objects.get(id = 1)
        
    if request.method == 'POST':

        client = Client.objects.get(name = request.POST['buyer'])
        commodity = Commodity.objects.get(name = request.POST['family'])

        
        dict = {}
        for key in request.POST:
            list = request.POST.getlist(key)
            dict.update({key: [val for val in list]})
        
        date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
        dict.update({"date": date})

        print request.POST
        
        if not request.POST['invoice_no'] or SaleInvoice.objects.filter(invoice_no = request.POST['invoice_no']).exists(): 

            context_dict = {"message": "Please enter a valid invoice number.",
                            "sale_form": sale_form,
                            "sale_detail_form": sale_detail_form,
                            "charges": charges,
                            }
            
            return render(request, 'partal/sale.html', context_dict)

        
        if request.POST['storage'] == str('Godown'):
            if commodity.net_stock_processed < float(request.POST['weight']) or commodity.bags_processed < int(request.POST['bags']):

                context_dict = {'message': 'Insufficient Processed commodity',
                                "sale_form": sale_form,
                                "sale_detail_form": sale_detail_form,
                                "charges": charges,
                                }

                return render(request, 'partal/sale.html', context_dict)

        if request.POST['storage'] == str('Cold'):
            if commodity.stock_cold < float(request.POST['weight']) or commodity.bags_cold < int(request.POST['bags']):

                context_dict = {'message': 'Insufficient Processed commodity',
                                "sale_form": sale_form,
                                "sale_detail_form": sale_detail_form,
                                "charges": charges,
                                }

                return render(request, 'partal/sale.html', context_dict)
            
        if request.POST['family'] != 'Pulse':
            num = 0
            for _ in dict['product']:
                product = Product.objects.get(name = _)
                if request.POST['storage'] == str('Godown'):
                    if product.net_stock_processed < float(dict['product_weight'][num]) or product.bags_processed < int(dict['product_bags'][num]):

                        context_dict = {'message': 'Insufficient Processed product',
                                        "sale_form": sale_form,
                                        "sale_detail_form": sale_detail_form,
                                        "charges": charges,
                        }

                        return render(request, 'partal/sale.html', context_dict)

                if request.POST['storage'] == str('Cold'):
                    if product.stock_cold < float(dict['product_weight'][num]) or product.bags_cold < float(dict['product_bags'][num]):
                        
                        context_dict = {'message': 'Insufficient Processed product',
                                        "sale_form": sale_form,
                                        "sale_detail_form": sale_detail_form,
                                        "charges": charges,
                        }

                        return render(request, 'partal/sale.html', context_dict)

                num += 1

        
        # Saving Sale Invoice
        sale_invoice = SaleInvoice(date = dict['date'],
                                   buyer = client,
                                   firm = request.POST['firm'],
                                   invoice_no = request.POST['invoice_no'],
                                   family = commodity,
                                   storage = request.POST['storage'],
                                   weight = request.POST['weight'],
                                   bags = request.POST['bags'],
                                   net_loose_amount = request.POST['net_loose_amount'],
                                   VAT = request.POST['VAT'],
                                   insurance = request.POST['insurance'],
                                   amount = request.POST['amount'],
                                   narration = request.POST['narration'])
        sale_invoice.save()

        # Updating Product Data and  Sale Inovice Detail
        if request.POST['family'] != 'Pulse':
            num = 0
            for _ in dict['product']:
                product = Product.objects.get(name = _)
                # Sale Invouce Detail
                sale_invoice_detail = SaleInvoiceDetail(invoice = sale_invoice,
                                                        product = product,
                                                        weight = dict[
                                                            'product_weight'][num],
                                                        rate = dict['product_rate'][num],
                                                        bags = dict['product_bags'][num],
                                                        amount = dict[
                                                            'product_amount'][num],)
                sale_invoice_detail.save()
            
                # Product Data
                if request.POST['storage'] == str('Godown'):
                    
                    product.net_stock_processed -= float(dict['product_weight'][num])
                    product.bags_processed -= int(dict['product_bags'][num])
                
                if request.POST['storage'] == str('Cold'):
                    
                    product.stock_cold -= float(dict['product_weight'][num])
                    product.bags_cold -= float(dict['product_bags'][num])

                if product.net_stock_processed < 0 or product.bags_processed < 0 or product.stock_cold < 0 or product.bags_cold < 0:

                    sale_invoice.delete()

                    if num > 0:
                        itr = 0
                        for val in dict['product']:
                            saved_product = Product.objects.get(name = val)
                            if itr != num:
                                if request.POST['storage'] == str('Godown'):
                                    
                                    saved_product.net_stock_processed += float(
                                        dict['product_weight'][itr])
                                    saved_product.bags_processed += int(
                                        dict['product_bags'][itr])
                                    
                                if request.POST['storage'] == str('Cold'):
                                    
                                    saved_product.stock_cold += float(
                                        dict['product_weight'][itr])
                                    saved_product.bags_cold += float(
                                        dict['product_bags'][itr])

                                saved_product.save()
                            
                            itr += 1

                            
                    context_dict = {'message': 'Insufficient Processed product',
                                    "sale_form": sale_form,
                                    "sale_detail_form": sale_detail_form,
                                    "charges": charges,
                    }

                    return render(request, 'partal/sale.html', context_dict)
                
                product.save()

                num += 1
        
        # Updating Commodity details
        if request.POST['storage'] == str('Godown'):

            commodity.net_stock_processed -= float(request.POST['weight'])
            commodity.bags_processed -= int(request.POST['bags'])

        if request.POST['storage'] == str('Cold'):

            commodity.stock_cold -= float(request.POST['weight'])
            commodity.bags_cold -= int(request.POST['bags'])
            
        commodity.save()

        # Updating Client details
        client.net_sale_weight += float(request.POST['weight'])
        client.net_sale_amount += int(request.POST['amount'])
        client.save()
        
        
        context_dict = {"message": "Sale invoice saved.",
                        "sale_form": sale_form,
                        "sale_detail_form": sale_detail_form,
                        "charges": charges,
                        }
        
        return render(request, 'partal/sale.html', context_dict)
                    
    else:
        # Not a POST Request
        context_dict = {"sale_form": sale_form,
                        "sale_detail_form": sale_detail_form,
                        "charges": charges,
                        }

        return render(request, 'partal/sale.html', context_dict)



# Process Entry
@login_required
def process_entry(request):

    context_dict = {}
    process_entry_form = ProcessEntryForm()

    if request.method == 'POST':

        date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
        final_out = request.POST.get('final_out', False)
        product = Product.objects.get(name = request.POST['product'])
        commodity = Commodity.objects.get(name = product.commodity.name)
        
        if product.net_stock_raw >= float(request.POST['weight_in']) and product.bags_raw >= int(request.POST['bags_in']):

            print final_out

            # Saving Entry Data
            new_entry = ProcessEntry(date = date,
                                     product = product,
                                     process = request.POST['process'],
                                     final_out = final_out,
                                     weight_in = request.POST['weight_in'],
                                     bags_in = request.POST['bags_in'],
                                     weight_out = request.POST['weight_out'],
                                     bags_out = request.POST['bags_out'],
                                     pulse_weight = request.POST['pulse_weight'],
                                     pulse_bags = request.POST['pulse_bags'],
                                     jhiri_weight = request.POST['jhiri_weight'],
                                     jhiri_bags = request.POST['jhiri_bags'],
                                     danthal_weight = request.POST['danthal_weight'],
                                     danthal_bags = request.POST['danthal_bags'],
                                     stone_weight = request.POST['stone_weight'],
                                     stone_bags = request.POST['stone_bags'],
                                     short_weight = request.POST['short_weight'],
                                     percentage_out = request.POST['percentage_out'],
                                     storage = request.POST['storage'],
                                     )
            new_entry.save()
            
            # Updating Product
            product.net_stock_raw -= float(request.POST['weight_in'])
            product.bags_raw -= int(request.POST['bags_in'])

            # Checking if product is dispatch ready 
            if final_out:
                # Update final processed fields
                if request.POST['storage'] == str('Godown'):
                    product.net_stock_processed += float(request.POST['weight_out'])
                    product.bags_processed += int(request.POST['bags_out'])

                else:
                    product.stock_cold += float(request.POST['weight_out'])
                    product.bags_cold += int(request.POSt['bags_out'])

            # Update raw fields
            else:
                product.net_stock_raw += float(request.POST['weight_out'])
                product.bags_raw += int(request.POST['bags_out'])

            product.save()
                
            # Updating Commodity
            commodity.net_stock_raw -= float(request.POST['weight_in'])
            commodity.bags_raw -= int(request.POST['bags_in'])

            # Checking if product is dispatch ready 
            if final_out:
                # Update final processed fields
                if request.POST['storage'] == str('Godown'):
                    commodity.net_stock_processed += float(request.POST['weight_out'])
                    commodity.bags_processed += int(request.POST['bags_out'])
                else:
                    commodity.stock_cold += float(request.POST['weight_out'])
                    commodity.bags_cold += int(request.POST['bags_out'])

            else:
                
                commodity.net_stock_raw += float(request.POST['weight_out'])
                commodity.bags_raw += int(request.POST['bags_out'])

            commodity.save()

            # Update pulse weight and bags
            try:
                pulse_detial = Commodity.objects.get(name = 'Pulse')

            except Commodity.DoesNotExist:

                pulse_detial = Commodity(name = 'Pulse',
                                         net_stock_processed = request.POST['pulse_weight'],
                                         bags_processed = request.POST['pulse_bags'],
                                         )
                pulse_detial.save()

            else:

                pulse_detial.net_stock_processed += float(request.POST['pulse_weight'])
                pulse_detial.bags_processed += int(request.POST['pulse_bags'])

                pulse_detial.save()

            
            # Update waste products
            update_waste_product('Jhiri', float(request.POST['jhiri_weight']),
                                 int(request.POST['jhiri_bags']))
            update_waste_product('Danthal', float(request.POST['danthal_weight']),
                                 int(request.POST['danthal_bags']))
            update_waste_product('Stone', float(request.POST['stone_weight']),
                                 int(request.POST['stone_bags']))

            process_entry_form = ProcessEntryForm()
            context_dict = {"message": "Entry Added",
                            "process_form": process_entry_form}
            
            return render(request, 'partal/process.html', context_dict)

        else:
            # Invalid Data
            context_dict = {"message": "Raw stock for " + product.name + " is less",
                            "process_form": process_entry_form,
                            }
            return render(request, 'partal/process.html', context_dict)

    else:
        # Not a POST Request
        context_dict = {"process_form": process_entry_form}

        return render(request, 'partal/process.html', context_dict)


# Function to update waste products
def update_waste_product(waste, waste_weight, waste_bags):

    try:
        waste = WasteProduct.objects.get(name = waste)

    except WasteProduct.DoesNotExist:

        waste = WasteProduct(name = waste,
                          weight = waste_weight,
                          bags = waste_bags,
                          )
        
        waste.save()

    else:

        waste.weight += waste_weight
        waste.bags += waste_bags

        waste.save()


# Reduce waste product data
def reduce_waste_detail(waste, waste_weight, waste_bags):

    waste = WasteProduct.objects.get(name = waste)

    waste.weight -= waste_weight
    waste.bags -= waste_bags
    
    waste.save()

        
