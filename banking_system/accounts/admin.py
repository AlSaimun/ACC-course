
from django.contrib import admin
from . import models 
# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin): 
        list_display = ['id', 'email']
        
@admin.register(models.BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin): 
        list_display = ['id', 'name',]
        
@admin.register(models.UserBankAccount)
class UserBankAccountAdmin(admin.ModelAdmin): 
        list_display = ['id', 'user', 'account_type', 'account_no', 'gender', 'birth_date', 'balance',]


@admin.register(models.UserAddress)
class UserAddressAdmin(admin.ModelAdmin): 
        list_display = ['id', 'user', 'street_address', 'city', 'postal_code', 'country']

# admin.site.register(models.UserAddress)
# admin.site.register(models.UserBankAccount)
# admin.site.register(models.BankAccountType)
# admin.site.register(models.User)