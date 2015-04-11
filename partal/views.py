from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime

from partal.models import *
from partal.forms import *

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
                                "firm_form": firm_form}

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
        context_dict = {"firm_form": firm_form}
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


# Purchase Invoice Entry
def purchase_invoice(request):

    context_dict = {}
    purchase_form = PurchaseForm()
    purchase_detail_form = PurchaseDetailForm()

    if request.method == 'POST':

        merchant = Firm.objects.get(name = request.POST['seller'])
        commodity = Commodity.objects.get(name = request.POST['family'])
        charges = RateDetail.objects.get(id = 1)
        
        dict = {}
        for key in request.POST:
            list = request.POST.getlist(key)
            dict.update({key: [val for val in list]})
        
        date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
        dict.update({"date": date})
        
        # Calculating Number of bags per entry
        bags = []
        b = 0
        for _ in dict['weight']:
            bag = float(_)/float(dict['bharti'][b])
            
            if bag % int(bag) >= 0.05:
                bag = int(bag) + 1
            else:
                bag = int(bag)

            bags.append(bag)
            b = b+1
        dict.update({"bags": bags})
        
        # Calculating Amount per entry
        amounts = []
        r = 0
        for _ in dict['weight']:
            amount = (float(_)*float(dict['rate'][r]))/100
            
            amounts.append(amount)
            r = r+1
        dict.update({"amounts": amounts})
        
        # Calculate Net Amount and saving data

        # Calculation Net Loose Amount
        net_loose_amount = 0
        for _ in dict['amounts']:
            net_loose_amount = net_loose_amount + _
        
        # Calculating Commission
        commission = (net_loose_amount*charges.commission)/100
        # Updating Merchant Commission
        if request.POST['firm'] == str('APB'):

            merchant.net_commission_APB = merchant.net_commission_APB + commission
            merchant.save()
        
        else:

            merchant.net_commission_KY = merchant.net_commission_KY + commission
            merchant.save()
        
        
        # Calculating Mandi Tax
        mandi_tax = (net_loose_amount*charges.mandi_tax)/100
        
        # Calculating Total number of bags
        total_bags = 0
        for _ in dict['bags']:
            total_bags = total_bags + _
        # Updating Commodity Bags
        commodity.bags_raw = commodity.bags_raw + total_bags
        commodity.save()

        # Calculating Total Weight in Kgs
        net_weight = 0
        for _ in dict['weight']:
            net_weight = net_weight + float(_)
        # Updating Merchant Net Weight
        merchant.net_purchase_weight = merchant.net_purchase_weight + net_weight
        merchant.save()
        # Updating Commodity Net Stock
        commodity.net_stock_raw = commodity.net_stock_raw + net_weight
        commodity.save()

        # Calculating Dharmada
        dharmada = (net_weight*charges.dharmada)/100

        # Calculating Association Charges
        association_charges = (net_weight*charges.association_charges)/100

        # Calculating Groos Amount (without VAT)
        gross_amount = net_loose_amount + commission + mandi_tax + dharmada + association_charges

        # Calculating VAT
        VAT = (gross_amount*charges.VAT)/100
        
        # Calculating Muddat
        muddat = (net_loose_amount*charges.muddat)/100
        
        # TDS Calculation
        if request.POST['firm'] == str('APB'):

            if merchant.net_commission_APB >= 5000:
                if (merchant.net_commission_APB - commission) < 5000:
                    TDS = (merchant.net_commission_APB*10)/100
                else:
                    TDS = (commission*10)/100
            else:
                TDS = 0
        else:
            
            if merchant.net_commission_KY >= 5000:
                if (merchant.net_commission_KY - commission) < 5000:
                    TDS = (merchant.net_commission_KY*10)/100
                else:
                    TDS = (commission*10)/100
            else:
                TDS = 0
        # Updating Merchant Monthly TDS
        if request.POST['firm'] == str('APB'):

            merchant.monthly_TDS_APB = float(merchant.monthly_TDS_APB) + TDS
            merchant.save()
       
        else:
            
            merchant.monthly_TDS_KY = float(merchant.monthly_TDS_KY) + TDS
            merchant.save()
       
        # Calculating Net Amount
        net_amount = (gross_amount + VAT) - muddat - TDS
        
        # Updating Merchant Net Amount
        merchant.net_purchase_amount = int(merchant.net_purchase_amount) + net_amount
        merchant.save()
        
        # Saving Purchase Invoice
        purchase_invoice = PurchaseInvoice(date = dict['date'],
                                           seller = merchant,
                                           seller_invoice_no = request.POST['seller_invoice_no'],
                                           family = commodity,
                                           weight = net_weight,
                                           bags = total_bags,
                                           net_loose_amount = net_loose_amount,
                                           commission = commission,
                                           mandi_tax = mandi_tax,
                                           association_charges = association_charges,
                                           dharmada = dharmada,
                                           muddat = muddat,
                                           VAT = VAT,
                                           TDS = TDS,
                                           amount = net_amount)
        purchase_invoice.save()

        # Updating Product Data, Purchase Inovice Detail and Daily Purchase
        num = 0
        for _ in dict['product']:
            # Product Data
            product = Product.objects.get(name = _)
            product.net_stock_raw = product.net_stock_raw + float(dict['weight'][num])
            product.bags_raw = product.bags_raw + dict['bags'][num]
            product.save()
            # Purchase Invouce Detail
            purchase_invoice_detail = PurchaseInvoiceDetail(invoice = purchase_invoice,
                                                            product = product,
                                                            weight = dict['weight'][num],
                                                            bharti = dict['bharti'][num],
                                                            rate = dict['rate'][num],
                                                            bags = dict['bags'][num],
                                                            amount = dict['amounts'][num],
                                                            )
            purchase_invoice_detail.save()
            num =num + 1
        
        # Daily Purchase
        entries = DailyPurchase.objects.filter(date = dict['date'])
        num = 0
        if not entries:
            for _ in dict['product']:
                product = Product.objects.get(name = _)
                try:
                    entry = DailyPurchase.objects.get(date = dict['date'], product = product)
                
                except DailyPurchase.DoesNotExist:

                    daily_purchase = DailyPurchase(date = dict['date'],
                                                   product = product,
                                                   product_weight = dict['weight'][num],
                                                   product_bags = dict['bags'][num],
                                                   total_purchase_amount = dict['amounts'][num],
                                                   )
                    daily_purchase.save()
                  
                    daily_purchase.rate = float(daily_purchase.total_purchase_amount)/float(daily_purchase.product_weight)
                    daily_purchase.save()

                    num = num + 1
                
                else:
                    
                    entry.product_weight = entry.product_weight + float(dict['weight'][num])
                    entry.product_bags = entry.product_bags + int(dict['bags'][num])
                    entry.total_purchase_amount = entry.total_purchase_amount + float(dict['amounts'][num])
                    entry.save()

                    entry.rate = float(entry.total_purchase_amount)/float(entry.product_weight)
                    entry.save()

                    num = num + 1

        else:
            for _ in dict['product']:
                product = Product.objects.get(name = _)
                
                try:
                    entry = DailyPurchase.objects.get(date = dict['date'], product = product)
            
                except DailyPurchase.DoesNotExist:
                    daily_purchase = DailyPurchase(date = dict['date'],
                                                   product = product,
                                                   product_weight = dict['weight'][num],
                                                   product_bags = dict['bags'][num],
                                                   total_purchase_amount = dict['amounts'][num],
                                                   )
                    daily_purchase.save()
                    
                    daily_purchase.rate = float(daily_purchase.total_purchase_amount)/float(daily_purchase.product_weight)
                    daily_purchase.save()
                    
                    num = num + 1
                    
                    
                else:
                    entry.product_weight = entry.product_weight + float(dict['weight'][num])
                    entry.product_bags = entry.product_bags + int(dict['bags'][num])
                    entry.total_purchase_amount = entry.total_purchase_amount + float(dict['amounts'][num])
                    entry.save()

                    entry.rate = float(entry.total_purchase_amount)/float(entry.product_weight)
                    entry.save()

                    num = num + 1

                    
        context_dict = {
            "invoice_no": purchase_invoice.id,
            "name": request.POST['seller'],
            "commodity":request.POST['family'],
            "products": dict['product'],
            "weights": dict['weight'],
            "bags": dict['bags'],
            "rates": dict['rate'],
            "amounts": dict['amounts'],
            "net_loose_amount": net_loose_amount,
            "commission": commission,
            "mandi_tax": mandi_tax,
            "dharmada":dharmada,
            "association_charges": association_charges,
            "gross_amount": gross_amount,
            "VAT": VAT,
            "muddat": muddat,
            "TDS": TDS,
            "net_amount": net_amount,
            }
        return render(request, 'partal/purchase.html', context_dict)
                    
    else:
        # Not a POST Request
        context_dict = {"purchase_form": purchase_form,
                        "purchase_detail_form": purchase_detail_form}

        return render(request, 'partal/purchase.html', context_dict)


# Sale Invoice
def sale_invoice(request):

    context_dict = {}
    sale_form = SaleForm()
    sale_detail_form = SaleDetailForm()

    if request.method == 'POST':

        client = Client.objects.get(name = request.POST['buyer'])
        commodity = Commodity.objects.get(name = request.POST['family'])
        charges = RateDetail.objects.get(id = 1)
        
        dict = {}
        for key in request.POST:
            list = request.POST.getlist(key)
            dict.update({key: [val for val in list]})
        
        date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
        dict.update({"date": date})
        
        # Calculating Number of bags per entry
        bags = []
        b = 0
        for _ in dict['weight']:
            bag = float(_)/float(dict['bharti'][b])
            
            if bag % int(bag) >= 0.05:
                bag = int(bag) + 1
            else:
                bag = int(bag)

            bags.append(bag)
            b = b+1
        dict.update({"bags": bags})
        
        # Calculating Amount per entry
        amounts = []
        r = 0
        for _ in dict['weight']:
            amount = (float(_)*float(dict['rate'][r]))/100
            
            amounts.append(amount)
            r = r+1
        dict.update({"amounts": amounts})
        
        # Calculate Net Amount and saving data

        # Calculation Net Loose Amount
        net_loose_amount = 0
        for _ in dict['amounts']:
            net_loose_amount = net_loose_amount + _
        
        # Calculating Total number of bags
        total_bags = 0
        for _ in dict['bags']:
            total_bags = total_bags + _
        # Updating Commodity Bags
        if request.POST['storage'] == str('Godown'):
           
            commodity.bags_processed = commodity.bags_processed - total_bags
            commodity.save()

        else:

            commodity.bags_cold = commodity.bags_cold - total_bags
            commodity.save()

        # Calculating Total Weight in Kgs
        net_weight = 0
        for _ in dict['weight']:
            net_weight = net_weight + float(_)
        # Updating Client Net Weight
        client.net_sale_weight = client.net_sale_weight + net_weight
        client.save()
        # Updating Commodity Net Stock
        if request.POST['storage'] == str('Godown'):
        
            commodity.net_stock_processed = commodity.net_stock_processed - net_weight
            commodity.save()

        else:

            commodity.stock_cold = commodity.stock_cold - net_weight
            commodity.save()

        # Calculating Insurance
        insurance = (net_loose_amount*charges.insurance)/100
        
        # Calculating VAT
        VAT = (net_loose_amount*charges.VAT)/100
        
        # Calculating Net Amount
        net_amount = net_loose_amount + VAT + insurance
        
        # Updating Client Net Amount
        client.net_sale_amount = int(client.net_sale_amount) + net_amount
        client.save()
        
        # Saving Sale Invoice
        sale_invoice = SaleInvoice(date = dict['date'],
                                   buyer = client,
                                   invoice_no = request.POST['invoice_no'],
                                   family = commodity,
                                   weight = net_weight,
                                   bags = total_bags,
                                   VAT = VAT,
                                   insurance = insurance,
                                   amount = net_amount)
        sale_invoice.save()

        # Updating Product Data and  Sale Inovice Detail
        num = 0
        for _ in dict['product']:
            # Product Data
            product = Product.objects.get(name = _)
            if request.POST['storage'] == str('Godown'):
           
                product.net_stock_processed = product.net_stock_processed - float(dict['weight'][num])
                product.bags_processed = product.bags_processed + dict['bags'][num]
                product.save()
            else:
                
                product.stock_cold = product.stock_cold - float(dict['weight'][num])
                product.bags_cold = product.bags_cold + dict['bags'][num]
                product.save()

            # Sale Invouce Detail
            sale_invoice_detail = SaleInvoiceDetail(invoice = sale_invoice,
                                                    product = product,
                                                    weight = dict['weight'][num],
                                                    bharti = dict['bharti'][num],
                                                    rate = dict['rate'][num],
                                                    bags = dict['bags'][num],
                                                    amount = dict['amounts'][num],
                                                    )
            sale_invoice_detail.save()
            num =num + 1
        
        
        context_dict = {
            "invoice_no": sale_invoice.invoice_no,
            "name": request.POST['buyer'],
            "commodity":request.POST['family'],
            "products": dict['product'],
            "weights": dict['weight'],
            "bags": dict['bags'],
            "rates": dict['rate'],
            "amounts": dict['amounts'],
            "net_loose_amount": net_loose_amount,
            "insurance": insurance,
            "VAT": VAT,
            "net_amount": net_amount,
            }
        return render(request, 'partal/sale.html', context_dict)
                    
    else:
        # Not a POST Request
        context_dict = {"sale_form": sale_form,
                        "sale_detail_form": sale_detail_form}

        return render(request, 'partal/sale.html', context_dict)



# Process Entry
def process_entry(request):

    context_dict = {}
    process_entry_form = ProcessEntryForm()

    if request.method == 'POST':

        date = request.POST['date_year'] + "-" + request.POST['date_month'] + "-" + request.POST['date_day']
        product = Product.objects.get(name = request.POST['product'])
        commodity = Commodity.objects.get(name = product.commodity.name)
        
        if product.net_stock_raw >= request.POST['weight_in'] and product.bags_raw >= request.POST['bags_in']:

            # Saving Entry Data
            new_entry = ProcessEntry(date = date,
                                     product = product,
                                     process = request.POST['process'],
                                     weight_in = request.POST['weight_in'],
                                     bags_in = request.POST['bags_in'],
                                     weight_out = request.POST['weight_out'],
                                     bags_out = request.POST['weight_out'],
                                     storage = request.POST['storage'],
                                     )
            new_entry.save()
            
            # Updating Product
            product.net_stock_raw = product.net_stock_raw - request.POST['weight_in']
            product.bags_raw = product.bags_raw - request.POST['bags_in']
            if request.POST['storage'] == str('Godown'):
                product.net_stock_processed = product.net_stock_processed + request.POST['weight_out']
                product.bags_processed = product.bags_processed + request.POST['bags_out']

            else:
                product.stock_cold = product.stock_cold + request.POST['weight_out']
                product.bags_cold = product.bags_cold + request.POSt['bags_out']
            product.save()
            
            # Updating Commodity
            commodity.net_stock_raw = commodity.net_stock_raw - request.POST['weight_in']
            commodity.bags_raw = commodity.bags_raw - request.POST['bags_in']
            if request.POST['storage'] == str('Godown'):
                commodity.net_stock_processed = commodity.net_stock_processed + request.POST['weight_out']
                commodity.bags_processed = commodity.bags_processed + request.POST['bags_out']

            else:
                commodity.stock_cold = commodity.stock_cold + request.POST['weight_out']
                commodity.bags_cold = commodity.bags_cold + request.POST['bags_out']
            commodity.save()

            process_entry_form = ProductEntryForm()
            context_dict = {"message": "Entry Added",
                            "process_entry_form": process_entry_form}
            
            return render(request, 'partal/process.html', context_dict)

        else:
            # Invalid Data
            context_dict = {"message": "Raw stock is less"}
            return render(request, 'partal/process.html', context_dict)

    else:
        # Not a POST Request
        context_dict = {"process_entry_form": process_entry_form}

        return render(request, 'partal/process.html', context_dict)


        
        
