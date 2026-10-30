from django.contrib import admin

from .models import Customer, Guarantor, Product, Sale, Payment

# Iska faida yeh hai ke jab aap Sale kholenge, payments niche hi nazar aa jayengi alag se kholna nahi parega
class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1 # Ek khali line hamesha dikhegi naya payment log karne ke liye
    fields = ('paid_by', 'amount_paid', 'date_paid')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'agreed_selling_price', 'total_paid_display', 'remaining_amount_display', 'status', 'sale_date')
    list_filter = ('status', 'sale_date')
    search_fields = ('customer__name', 'customer__cnic', 'product__name')
    inlines = [PaymentInline] # Sales ke page ke andar hi payments table show hoga

    # Django Admin me @property direct show nahi hoti, isliye we use methods:
    def total_paid_display(self, obj):
        return f"Rs. {obj.total_paid:,.2f}"
    total_paid_display.short_description = "Total Paid (Advance + Installments)"

    def remaining_amount_display(self, obj):
        return f"Rs. {obj.remaining_amount:,.2f}"
    remaining_amount_display.short_description = "Remaining Balance"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_no', 'cnic')
    search_fields = ('name', 'cnic', 'phone_no')

@admin.register(Guarantor)
class GuarantorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_no', 'cnic')
    search_fields = ('name', 'cnic')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'actual_price', 'selling_price', 'profit_margin')
    
    def profit_margin(self, obj):
        margin = obj.selling_price - obj.actual_price
        return f"Rs. {margin:,.2f}"
    profit_margin.short_description = "Expected Profit"
