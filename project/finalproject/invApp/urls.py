from django.urls import path

from . import views

urlpatterns = [
  path('', views.home_view, name="home"),

  path("accounts/login/", views.login_view, name="login"),

  path("accounts/logout/", views.logout_view, name="logout"),

  path("accounts/register/", views.register_view, name="register"),

  path('add-product/', views.product_create_view, name="add-product"),

  path('product-list/', views.product_list_view, name="product-list"),

  path('update/<int:productid>/', views.product_update_view, name="product-update"),

  path('delete/<int:productid>/', views.product_delete_view, name="product-delete"),

  path('supplier/', views.supplier_list, name="supplier-list"),

  path('supplier-update/<int:id>/', views.supplier_update,
  name="supplier-update"),

  path('order-list/', views.order, name='order-list'),

  path('order-add/',views.order_add, name='order-add'),

  path('order-update/<int:id>/',views.order_update, name='order-update'),

  path('order-delete/<int:id>/',views.order_delete, name='order-delete'),

  path('purchase-list/',views.purchase_orders,name="purchase-orders-list"),

  path('purchase-add/',views.purchase_add, name='purchase-add'),

  path('purchase-update/<int:id>/',views.purchase_update, name='purchase-update'),

  path('purchase-delete/<int:id>/', views.purchase_delete, name='purchase-delete'),

  path('dashboard/', views.dashboard, name="dashboard"),
]
