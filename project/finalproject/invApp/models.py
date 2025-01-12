from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
  product_id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  sku = models.CharField(max_length=50, unique=True)
  price = models.FloatField()
  cost = models.FloatField()
  quantity = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  cost_quantity = models.FloatField(null=True, blank=True)
  supplier = models.CharField(max_length=100)
  units_sold = models.IntegerField(default=0)

  def __str__(self):
    return f"{self.name} - {self.supplier}"

class Supplier(models.Model):
  id = models.AutoField(primary_key=True)
  supplier_name = models.CharField(max_length=100)
  contact = models.CharField(unique=True, max_length = 50)
  supplies = models.TextField(blank=True, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.supplier_name


class Orders(models.Model):
    order_no = models.IntegerField(unique=True)
    customer_name = models.CharField(max_length=100)
    total_amount = models.FloatField(null=True, blank=True)
    date = models.DateField()
    deadline = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_cost = models.FloatField(null=True, blank=True)
    number_of_products = models.IntegerField(null=True, blank = True)

    # Add choices to these fields
    STATUS_CHOICES = [
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid')
    ]
    DELIVERY_CHOICES = [
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default = "not_paid")
    delivery = models.CharField(max_length=50, choices=DELIVERY_CHOICES, default = "packed")

    products = models.ManyToManyField('Product', related_name='orders')

    def __str__(self):
        return self.customer_name


class PurchaseOrder(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_no = models.IntegerField(unique=True)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    supplier_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    total_amount = models.FloatField()
    date = models.DateField()
    deadline = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('not_received', 'Not Received'),
        ('received', 'Received')
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_received')  # Provide a default value

    def __str__(self):
        return self.product_name

