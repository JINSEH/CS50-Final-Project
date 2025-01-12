import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from .models import *

class OrderFilter(django_filters.FilterSet):
  start_date = DateFilter(
    field_name="date",
    lookup_expr="gte",
    widget=forms.DateInput(attrs={
    'type': 'date',
    'class': 'form-control',
    'placeholder': 'Start Date'
  }),)
  end_date = DateFilter(
    field_name="deadline",
    lookup_expr = "lte",
    widget=forms.DateInput(attrs={
    'type': 'date',
    'class': 'form-control',
    'placeholder': 'End Date'
  }),)
  customer_name = CharFilter(field_name="customer_name", lookup_expr="icontains")

  class Meta:
    model = Orders
    exclude = ['total_amount', 'date','deadline', 'user', 'products', 'total_cost', 'number_of_products',]

class ProductFilter(django_filters.FilterSet):
  name = CharFilter(field_name="name", lookup_expr="icontains")
  supplier = CharFilter(field_name="supplier", lookup_expr="icontains")
  class Meta:
    model = Product
    exclude = ['user','cost_quantity', 'price', 'cost','quantity', 'units_sold']
