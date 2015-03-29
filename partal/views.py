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

    
