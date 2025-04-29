from django.contrib import admin
from .models import Owner, Property, Tenant, Contract, Payment
from django.contrib import admin
from .models import Owner, Property, Tenant, Contract, Payment

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone')
    search_fields = ('last_name', 'first_name', 'email', 'phone')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'price', 'is_available')
    list_filter = ('property_type', 'is_available')
    raw_id_fields = ('owner',)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone')
    search_fields = ('last_name', 'first_name', 'email')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'tenant', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    raw_id_fields = ('property', 'tenant')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'amount', 'payment_date', 'is_confirmed')
    list_filter = ('is_confirmed',)
    raw_id_fields = ('contract',)