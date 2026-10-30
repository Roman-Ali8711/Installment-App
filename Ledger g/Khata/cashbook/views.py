from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Sale, Payment
from django.contrib import messages
from decimal import Decimal, InvalidOperation  # 👈 Yeh import laazmi add karein!
from django.db import transaction 

def dashboard_view(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'cashbook/dashboard.html', context)

def customer_detail_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    sales = customer.sales.all()
    return render(request, 'cashbook/customer_detail.html', {'customer': customer, 'sales': sales})

def add_payment_view(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    
    if request.method == 'POST':
        paid_by = request.POST.get('paid_by')
        amount_paid_raw = request.POST.get('amount_paid')
        date_paid = request.POST.get('date_paid')
        
        try:
            # 👈 float ki jagah Decimal me convert kiya taake database accuracy barqarar rahe
            amount_paid = Decimal(amount_paid_raw)
            
            if amount_paid > sale.remaining_amount:
                messages.error(request, f"Error: Baqaya balance Rs. {sale.remaining_amount} hai, aap zyada raqam add kar rahe hain!")
                return render(request, 'cashbook/add_payment.html', {'sale': sale})
            
            # Save payment record safely
            Payment.objects.create(
                sale=sale,
                paid_by=paid_by,
                amount_paid=amount_paid,
                date_paid=date_paid
            )
            
            # Check if contract is fully paid off
            if (sale.remaining_amount - amount_paid) <= 0:
                sale.status = 'completed'
                sale.save()
                
            messages.success(request, "Kist kamyabi se jama ho gayi!")
            return redirect(f'/customer/{sale.customer.id}/')
            
        except (ValueError, InvalidOperation):
            messages.error(request, "Meharbani kar ke sahi raqam enter karein.")
            
    return render(request, 'cashbook/add_payment.html', {'sale': sale})