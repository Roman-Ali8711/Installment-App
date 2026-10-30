from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class Customer(models.Model):
    name= models.CharField(max_length=255)  
    cnic= models.CharField(max_length=15,unique=True)
    phone_no= models.CharField(max_length=15,unique=True)
    address= models.TextField()
    def __str__(self):
        return f"{self.name} ({self.cnic})"

class Guarantor(models.Model):
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    cnic = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"Guarantor: {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2) # Cost price
    selling_price = models.DecimalField(max_digits=10, decimal_places=2) # Base retail price

    def __str__(self):
        return self.name

class Sale(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    guarantor = models.ForeignKey(Guarantor, on_delete=models.SET_NULL, null=True, blank=True)
    
    total_installments = models.IntegerField(help_text="Total number of months/installments")
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    agreed_selling_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Final price for this installment deal")
    
    sale_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    @property
    def monthly_installment_amount(self):
        """Calculates how much the customer needs to pay per month"""
        net_installment_amount = self.agreed_selling_price - self.advance_payment
        if self.total_installments > 0:
            return round(net_installment_amount / self.total_installments, 2)
        return 0

    @property
    def expected_installments_paid_till_now(self):
        """Calculates how many installments should have been paid based on dates"""
        from datetime import date
        today = date.today()
        
        # Calculate months passed since sale
        years_diff = today.year - self.sale_date.year
        months_diff = today.month - self.sale_date.month
        total_months_passed = (years_diff * 12) + months_diff
        
        # dynamic limits bound karne ke liye
        if total_months_passed < 0:
            return 0
        return min(total_months_passed, self.total_installments)
    
    def __str__(self):
        return f"{self.customer.name} - {self.product.name} ({self.sale_date})"

    @property
    def total_paid(self):
        # Calculates all payments made for this sale
        payments_sum = self.payments.aggregate(total=models.Sum('amount_paid'))['total'] or 0
        return self.advance_payment + payments_sum

    @property
    def remaining_amount(self):
        # Business logic: balance updates automatically
        return self.agreed_selling_price - self.total_paid

class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments')
    paid_by = models.CharField(max_length=255, help_text="Name of the individual handing over the money")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()

    def __str__(self):
        return f"Payment of {self.amount_paid} for Sale ID {self.sale.id}"    
    
# Is method ko app 'Sale' class ke andar add kar sakte hain
def clean(self):
    from django.core.exceptions import ValidationError
    
    # Check agar is customer ka koi purana khata 'overdue' to nahi?
    overdue_sales = Sale.objects.filter(customer=self.customer, status='overdue')
    if overdue_sales.exists():
        raise ValidationError(
            f"Alert! {self.customer.name} ka purana balance overdue hai. "
            f"Pehle purani installment clear karein!"
        )    
