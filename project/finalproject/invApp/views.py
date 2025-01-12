from django.shortcuts import render, redirect
from .forms import RegisterForm,ProductForm, SupplierForm, OrderForm,PurchaseOrderForm
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .models import Product, Supplier, Orders, PurchaseOrder
from .filters import OrderFilter, ProductFilter
from django.db.models import Sum
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

#This is for the registration form for authorisation.
def register_view(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get("username")
      password = form.cleaned_data.get("password")
      user = User.objects.create_user(username = username, password=password)
      login(request, user)
      return redirect("home")

    else:
      # Form is not valid, re-render the form with errors
      return render(request, 'accounts/register.html', {'form': form})

  else:
    form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})

#This is for login
def login_view(request):
  error_message = None
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")
    #Authenticate checks against the user model to check the credentials

    #If the credentials are correct it returns a user object, representing the authenticated user

    #If credentials are wrong, it returns None
    user = authenticate(request, username=username, password=password)
    if user is not None:
      #If authenticated, a session will be created using login()
      login(request, user)
      next_url = request.POST.get('next') or request.GET.get("next") or 'home'
      return redirect(next_url)

    else:
      #Invalid credentials
      error_message = "Invalid Credentials!"

  return render(request, "accounts/login.html", {"error" : error_message})

#This is for the logout
def logout_view(request):
  if request.method == "POST":
    logout(request)
    return redirect("login")
  else:
    return render(request, "accounts/logout.html")

#Home view
@login_required
def home_view(request):
  return render(request, 'auth1_app/home.html')


#For product listing:
def product_create_view(request):
  if request.method == "POST":
      form = ProductForm(request.POST, user=request.user)
      if form.is_valid():
          product = form.save(commit=False)  # Do not save to the database yet
          product.user = request.user
          product.units_sold = 0

          # Calculate cost * quantity
          cost = form.cleaned_data.get("cost")
          quantity = form.cleaned_data.get("quantity")
          product.cost_quantity = cost * quantity

          product.save()
          return redirect('add-product')  # Replace with your desired redirect URL
      else:
          print(form.errors)
  else:
      form = ProductForm(user=request.user)

  return render(request, 'product_list/product_form.html', {'form': form})

def product_list_view(request):
  #Get user's object
  user=request.user
  #Get user id associated with database
  products = Product.objects.filter(user=user).order_by('-supplier')
  myFilter = ProductFilter(request.GET, queryset = products)
  products = myFilter.qs
  #Pagination Logic
  paginator = Paginator(products, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'products' : page_obj,
    'myFilter' : myFilter,
  }
  return render(request, 'product_list/product-list.html', context)

def product_update_view(request, productid):
  user = request.user
  product = Product.objects.get(product_id=productid, user=user)
  if request.method == "POST":
      form = ProductForm(request.POST, instance=product, user=user)
      if form.is_valid():
          product = form.save(commit=False)
          cost = form.cleaned_data.get("cost")
          quantity = form.cleaned_data.get("quantity")

          product.cost_quantity = cost * quantity

          product.save()
          return redirect('product-list')
  else:
      form = ProductForm(instance=product, user=user)

  return render(request, 'product_list/product_form.html', {'form': form})


def product_delete_view(request, productid):
  user = request.user
  product = Product.objects.get(product_id = productid, user=user)
  if request.method == "POST":
    product.delete()
    return redirect('product-list')
  return render(request, 'product_list/product_confirm_delete.html', {'product' : product})

#For suppliers
def supplier_list(request):
  user = request.user
  suppliers = Supplier.objects.filter(user=user)

  if request.method == 'POST':
    form =  SupplierForm(request.POST)
    if form.is_valid():
      supplier = form.save(commit=False)
      supplier.user = user
      supplier.save()
      return redirect('supplier-list')

  else:
    form = SupplierForm()

  context = {
    'form' : form,
    'suppliers' : suppliers
  }
  return render(request, 'suppliers/supplier-list.html', context)

def supplier_update(request, id):
  user = request.user
  suppliers = Supplier.objects.filter(user=user)

  try:
    supplier = Supplier.objects.get(id=id, user=user)
  except Supplier.DoesNotExist:
     return redirect('supplier-list')

  form = SupplierForm(instance=supplier)
  if request.method == 'POST':
    if 'Delete' in request.POST:
      supplier.delete()
      return redirect('supplier-list')

    form = SupplierForm(request.POST, instance=supplier)
    if form.is_valid():
      form.save()
      return redirect('supplier-list')

  context = {
    'form' : form,
    'suppliers' : suppliers
  }

  return render(request, 'suppliers/supplier-list-update.html', context)

#For customer orders
def order_add(request):
    form = OrderForm(user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)  # Pass the user when instantiating the form
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            selected_products = form.cleaned_data["products"]
            total_cost = 0
            total_amount = 0
            number_of_product = 0
            out_of_stock = []  # List to collect out-of-stock products

            for product in selected_products:
                total_cost += product.cost
                total_amount += product.price
                number_of_product += 1
                product.units_sold += 1

                if product.quantity > 0:
                    product.quantity -= 1
                    product.save()
                else:
                    out_of_stock.append(product.name)  # Collect out-of-stock product names

            if out_of_stock:
                messages.error(request, f"These products are out of stock: {', '.join(out_of_stock)}")

            order.total_amount = total_amount
            order.total_cost = total_cost
            order.number_of_products = number_of_product
            order.save()

            order.products.set(selected_products)
            form.save_m2m()
            return redirect('order-list')

    context = {
        'form': form,
    }
    return render(request, 'cust_orders/order-add.html', context)

def order(request):
  user = request.user
  orders = Orders.objects.filter(user = user).order_by('status','-delivery','date')
  totals = Orders.objects.filter(user=user).aggregate(total_amount = Sum('total_amount'), total_cost = Sum('total_cost'), number_of_products = Sum('number_of_products'))
  stock_on_hand = Product.objects.filter(user=user).aggregate(cost_quantity = Sum("cost_quantity"))

  if totals['total_amount'] == None:
    total_amount = 0

  else:
    total_amount = totals['total_amount']


  if totals['total_cost'] == None:
    total_cost = 0

  else:
    total_cost = totals['total_cost']


  if totals['number_of_products'] == None:
    number_of_products = 0

  else:
    number_of_products = totals['number_of_products']

  if stock_on_hand['cost_quantity'] == None:
    cost_quantity = 0

  else:
    cost_quantity = stock_on_hand['cost_quantity']

  myFilter = OrderFilter(request.GET, queryset=orders)
  orders = myFilter.qs

  #Pagination Logic
  paginator = Paginator(orders, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'orders' : page_obj,
    'myFilter' : myFilter,
    'total_amount' : total_amount,
    'total_cost' : total_cost,
    'number_of_products' : number_of_products,
    'cost_quantity' : cost_quantity,
  }
  return render(request, 'cust_orders/order-list.html', context)


def order_update(request, id):
    user = request.user
    order = Orders.objects.get(id=id, user=user)
    form = OrderForm(instance=order)
    if order.status == 'paid' and order.delivery == 'delivered':
        messages.warning(request, "This order has already been completed and cannot be updated.")
        return render(request, "cust_orders/order_completed.html")

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order, user=user)  # Pass the user to filter products
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            order.save()

            total_cost = 0
            total_amount = 0
            number_of_products = 0
            selected_products = form.cleaned_data["products"]
            out_of_stock = []

            for product in selected_products:
                total_cost += product.cost
                total_amount += product.price
                number_of_products += 1

                if product.quantity > 0:
                    product.quantity -= 1
                    product.save()
                else:
                    out_of_stock.append(product.name)

            if out_of_stock:
                messages.error(request, f"These products are out of stock: {', '.join(out_of_stock)}")

            order.total_amount = total_amount
            order.total_cost = total_cost
            order.number_of_products = number_of_products
            order.save()

            order.products.set(selected_products)
            form.save_m2m()
            return redirect('order-list')

    context = {
        'form': form,
    }
    return render(request, 'cust_orders/order-add.html', context)

def order_delete(request, id):
  user = request.user
  order = Orders.objects.get(id = id, user=user)
  if request.method == 'POST':
    order.delete()
    return redirect('order-list')
  context = {
    'order' : order
  }
  return render(request, 'cust_orders/order_confirm_delete.html',context)

#For company purchases
def purchase_orders(request):
  user = request.user
  purchases = PurchaseOrder.objects.filter(user=user).order_by('-status').reverse()

  #Pagination Logic
  paginator = Paginator(purchases, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'purchases' : page_obj,
  }
  return render(request, 'our_orders/purchase-order-list.html', context)

def purchase_add(request):
    form = PurchaseOrderForm(user=request.user)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, user=request.user)
        user = request.user
        if form.is_valid():
            # Save the form instance without committing to the DB yet
            purchase = form.save(commit=False)
            purchase.user = user

            # Get quantity for later
            quantity = form.cleaned_data["quantity"]

            # Get the selected product from the form
            selected_product = form.cleaned_data["products"]
            print(selected_product)
            # Calculate total amount
            total_amount = selected_product.cost * quantity

            # Save product details
            purchase.product_name = selected_product.name
            purchase.supplier_name = selected_product.supplier

            # Get supplier contact info
            supplier_info = Supplier.objects.get(supplier_name=selected_product.supplier, user=user)

            purchase.contact = supplier_info.contact

            # Save total amount
            purchase.total_amount = total_amount

            # Save purchase object
            purchase.save()

            #Get product instance
            product = Product.objects.get(name = selected_product.name, user = user)

            #Update the quantity

            return redirect('purchase-orders-list')

        else:
            print(form.errors)  # Print form errors to the console

    context = {'form': form}
    return render(request, 'our_orders/purchase-add.html', context)

def purchase_update(request, id):
  purchase = PurchaseOrder.objects.get(id = id)
  form = PurchaseOrderForm(instance = purchase)
  user=request.user

  if purchase.status == "received":
        # Redirect to the list view with a warning message
        messages.warning(request, "This purchase order has already been received and cannot be updated.")
        return render(request, "our_orders/purchase_received.html")

  if request.method == 'POST':
    form = PurchaseOrderForm(request.POST, instance=purchase)
    if form.is_valid():
        status = form.cleaned_data["status"]

        if status == "not_received":
          print("Status is not received")

        #If status is received, update product quantity
        else:
          print("Status is received")
          product_name = purchase.product_name
          print(product_name)
          supplier = purchase.supplier_name
          print(supplier)
          product = Product.objects.get(user=user, name = product_name, supplier = supplier)
          product.quantity += purchase.quantity
          product.save()

        form.save()
        return redirect('purchase-orders-list')

    else:
        print(form.errors)  # Print form errors to the console

  context = {
    'form' : form,
    'purchase' : purchase,
  }
  return render(request, 'our_orders/purchase-update.html', context)

def purchase_delete(request, id):
  purchase = PurchaseOrder.objects.get(id=id)
  if request.method == 'POST':
    purchase.delete()
    return redirect('purchase-orders-list')
  context = {
    'purchase' : purchase,
  }
  return render(request, 'our_orders/purchase_confirm_delete.html', context)

#For the dashboard
def dashboard(request):
  user = request.user
  packed_orders_count = Orders.objects.filter(delivery='packed', user=user).count()
  shipped_orders_count = Orders.objects.filter(delivery='shipped', user=user).count()
  delivered_orders_count = Orders.objects.filter(delivery='delivered', user=user).count()

  totals= Product.objects.filter(user=user).aggregate(total_quantity = Sum('quantity'))
  total_quantity = totals['total_quantity']

  try:
    top_product = Product.objects.filter(user=user).order_by('-units_sold').first()

  except IndexError:
    top_product=None

  try:
    second_product = Product.objects.filter(user=user).order_by('-units_sold')[1]

  except IndexError:
    second_product=None

  try:
    third_product = Product.objects.filter(user=user).order_by('-units_sold')[2]

  except IndexError:
    third_product=None

  context = {
    "packed" : packed_orders_count,
    "shipped" : shipped_orders_count,
    "delivered" : delivered_orders_count,
    "total_quantity" : total_quantity,
    "top" : top_product,
    "second" : second_product,
    "third" : third_product,
  }
  return render(request, 'auth1_app/dashboard.html', context)
