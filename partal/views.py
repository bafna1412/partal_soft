from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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



# Delete Purchase detail
@login_required
def purchase_delete(request, entry_id):

    #Fetch the entry to be deleted
    entry = PurchaseInvoiceDetail.objects.get(id = entry_id)
    firms = Firm.objects.filter(group = entry.seller.group)
    entries = []

    # Check date of entry. Only current date entries can be deleted
    for firm in firms:
        
        invoices = PurchaseInvoice.objects.filter(date = entry.date, seller = firm.name)
        if invoices:
            entries.append(invoices)

    # Make changes only if invoice is not made
    if not entries:
        
        #Make changes to daily purchase
        daily_purchase = DailyPurchase.objects.get(date = entry.date, product = entry.product)

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
                message = "No entries for this date"
                
                context_dict = {"message": message,
                                "date": date,
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
    entries = PurchaseInvoiceDetail.objects.filter(seller = seller)
    
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
                print request.POST['paid_with']
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
            # Errors in form
            context_dict = {"sale_estimate_form": sale_estimate_form}

    return render(request, 'partal/estimatesale.html', context_dict)



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
@login_required
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


        
        
