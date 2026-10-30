from django.urls import path
from . import views

app_name = 'cashbook'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('customer/<int:customer_id>/', views.customer_detail_view, name='customer_detail'),
    path('sale/<int:sale_id>/payment/add/', views.add_payment_view, name='add_payment'),
]