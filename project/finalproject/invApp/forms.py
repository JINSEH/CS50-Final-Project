from django import forms
from django.contrib.auth.models import User
from .models import Product, Supplier, Orders, PurchaseOrder

#For user registration
class RegisterForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput(attrs ={
    "autocomplete" : "off",
    "label" : "password",
    "class" : "form-control mb-3",
    }
    )
  )

  password_confirm = forms.CharField(widget=forms.PasswordInput(attrs ={
    "autocomplete" : "off",
    "label" : "password_confirm",
    "class" : "form-control mb-3",
    }
    )
  )

  class Meta:
    model = User
    fields = ['username', 'password', 'password_confirm']
    widgets = {
      'username' : forms.TextInput(attrs = {
        "autocomplete" : "off",
        "username" : "username",
        "class" : "form-control mb-3",
      })
    }

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    password_confirm = cleaned_data.get("password_confirm")
    #Check if the password and password confirm exists and passwords match.
    if password and password_confirm and password != password_confirm:
      raise forms.ValidationError("Passwords do not match!")
    return cleaned_data

class ProductForm(forms.ModelForm):
  supplier = forms.ModelChoiceField(
  queryset=Supplier.objects.none(),
  widget=forms.RadioSelect(),
  label='Supplier'
  )

  class Meta:
    model = Product

    exclude = ['user','cost_quantity', 'units_sold']

    labels = {
      'product_id' :'Product_ID',
      'name' : 'Product Name',
      'sku' : 'SKU',
      'price' : 'Price',
      'cost' : "Cost",
      'quantity' : 'Quantity',
    }

    widgets = {
      'product_id': forms.NumberInput(attrs={'placeholder' : 'e.g. 1' , 'class' : 'form-control'}),

      'name': forms.TextInput(attrs={'placeholder' : 'e.g. Shoes' , 'class' : 'form-control'}),

      'sku': forms.TextInput(attrs={'placeholder' : 'e.g. S12345' , 'class' : 'form-control'}),

      'price': forms.NumberInput(attrs={'placeholder' : 'e.g. 19.99' , 'class' : 'form-control'}),

      'cost': forms.NumberInput(attrs={'placeholder' : 'e.g. 29.99' , 'class' : 'form-control'}),

      'quantity': forms.NumberInput(attrs={'placeholder' : 'e.g. 10' , 'class' : 'form-control'}),
    }

  def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['supplier'].queryset = Supplier.objects.filter(user=user)

class SupplierForm(forms.ModelForm):
  class Meta:
    model = Supplier
    exclude = ['user']
    labels = {
      'supplier_name' : 'Supplier Name',
      'contact'  : "Contact Information",
      'supplies' : 'Supplies'
    }

    widgets = {
      'supplier_name' : forms.TextInput(attrs={
        'placeholder' : 'E.g. ST Logistics', 'class' : "form-control"}),

      'contact' : forms.TextInput(attrs={
        'placeholder' : 'E.g. +1-329-012-210', 'class' : "form-control"}),

      'Supplies' : forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Electronics, TV, Shoes',})
      }


class OrderForm(forms.ModelForm):
  STATUS_CHOICES = [
    ('not_paid', 'Not Paid'),
    ('paid', 'Paid')
  ]

  DELIVERY_CHOICES = [
    ('packed', 'Packed'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
  ]

  status = forms.ChoiceField(
    choices=STATUS_CHOICES,
    widget=forms.RadioSelect(attrs={'class':'status-radio'}),
    label='Status'
  )

  delivery = forms.ChoiceField(
    choices=DELIVERY_CHOICES,
    widget=forms.RadioSelect(attrs={'class':'delivery-radio'}),
    label='Delivery'
  )

  # Add a field to select products
  products = forms.ModelMultipleChoiceField(
    queryset=Product.objects.none(),
    widget=forms.CheckboxSelectMultiple(),
    label='Products'
  )

  class Meta:
    model = Orders
    exclude = ['user', 'total_cost', 'total_amount', 'number_of_products']
    labels = {
      'order_no' : 'Order#',
      'customer_name' : 'Customer Name',
      'date' : 'Date',
      'deadline' : 'Delivery Deadline',
    }

    widgets = {
      'order_no' : forms.NumberInput(attrs={
        'placeholder' : 'E.g. 003594', 'class' : "form-control"}),

      'customer_name' : forms.TextInput(attrs={
        'placeholder' : 'E.g. Leong Tock Koh', 'class' : "form-control"}),

      'total_amount' : forms.NumberInput(attrs={
        'placeholder' : 'E.g. 580.34', 'class' : "form-control"}),

      'date' : forms.DateInput(attrs={'class': 'form-control' ,'placeholder': 'E.g. 17 Sep 2025',
      'type': 'date',
      }),

      'deadline' : forms.DateInput(attrs={'class': 'form-control' ,'placeholder': 'E.g. 23 Sep 2025',
      'type': 'date',
      }),
      }

  def clean_deadline(self):
    date = self.cleaned_data.get('date')
    deadline = self.cleaned_data.get('deadline')
    if deadline and date and deadline < date:
        raise forms.ValidationError("Deadline cannot be earlier than the date!")
    return deadline

  def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super(OrderForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['products'].queryset = Product.objects.filter(user=user)  # Use the user to filter products

class PurchaseOrderForm(forms.ModelForm):
  STATUS_CHOICES = [
    ('not_received', 'Not Received'),
    ('received', 'Received')
  ]

  status = forms.ChoiceField(
    choices=STATUS_CHOICES,
    widget=forms.RadioSelect(attrs={'class':'status-radio'}),
    label='Status'
  )

   # Add a field to select products
  products = forms.ModelChoiceField(
    queryset=Product.objects.none(),
    widget=forms.RadioSelect(),
    label='Products'
  )

  class Meta:
    model = PurchaseOrder
    exclude = ['user','supplier_name', 'contact','total_amount','product_name']
    labels = {
      'invoice_no' : 'Invoice No.',
      'quantity' : 'Quantity',
      'total_amount' : 'Total Amount',
      'date' : 'Date',
      'deadline' : 'Date to receive by',
    }

    widgets = {
      'invoice_no' : forms.NumberInput(attrs={
      'placeholder' : 'E.g. 1001', 'class' : "form-control"}),

      'quantity' : forms.NumberInput(attrs={
      'placeholder' : 'E.g. 20', 'class' : "form-control"}),

      'date' : forms.DateInput(attrs=
      {'class': 'form-control' ,
       'placeholder': 'E.g. 17 Sep 2025',
       'type': 'date'}),

      'deadline' : forms.DateInput(attrs={
         'class': 'form-control' ,
         'placeholder': 'E.g. 23 Sep 2025',
         'type': 'date'}),
      }
  def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['products'].queryset = Product.objects.filter(user=user)  # Filter products for the logged-in user

        # If the instance (purchase order) already exists, make some fields readonly
        if self.instance.pk:
            self.fields['quantity'].widget.attrs['readonly'] = 'readonly'
            self.fields['invoice_no'].widget.attrs['readonly'] = 'readonly'
            self.fields['date'].widget.attrs['readonly'] = 'readonly'
            self.fields['deadline'].widget.attrs['readonly'] = 'readonly'
            if 'products' in self.fields:
                del self.fields['products']  # Remove the products field if you don't want to display it
