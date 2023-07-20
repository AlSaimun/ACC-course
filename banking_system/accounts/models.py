import datetime
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import UserManager

from .constants import GENDER_CHOICES
# Create your models here.

class User(AbstractUser): 
        ''' custom user class (use AbstractUser for creatig custom user model) '''
        
        # using the custom manager for user model 
        objects = UserManager()
        username = None
        email = models.EmailField(unique=True, null=False, blank=False)
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []
        
        def __str__(self): 
                return self.email 
        
        @property
        def balance(self): 
                if hasattr(self, 'account'): 
                        return self.account.balance
                return 0 
        
# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True, null=False, blank=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email

#     @property
#     def balance(self):
#         if hasattr(self, 'account'):
#             return self.account.balance
#         return 0



        
class BankAccountType(models.Model): 
        ''' model to handle the type of bank account '''
        name = models.CharField(max_length=30)
        maximum_withdrawl_amount = models.DecimalField(default=50000, max_digits=8, decimal_places=2)
        
        def __str__(self): 
                return self.name 
        
        
class UserBankAccount(models.Model): 
        ''' model for user bank account  '''
        user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
        account_type = models.ForeignKey(BankAccountType, related_name='account_type', on_delete=models.CASCADE)
        account_no = models.PositiveIntegerField(unique=True)
        gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
        birth_date = models.DateField(null=False, blank=False)
        balance = models.DecimalField(default=0, max_digits=10, decimal_places =2)
        initial_deposite_date = models.DateTimeField(default=datetime.datetime.now())

        def __str__(self): 
                return str(self.account_no)
        
class UserAddress(models.Model): 
        ''' model for user address '''
        user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
        street_address = models.CharField(max_length=150)
        city = models.CharField(max_length=30)
        postal_code = models.IntegerField()
        country = models.CharField(max_length=30)
        
        def __str__(self): 
                return self.user.email 
        
        
        
        
        
        
# from decimal import Decimal

# from django.contrib.auth.models import AbstractUser
# from django.core.validators import (
#     MinValueValidator,
#     MaxValueValidator,
# )
# from django.db import models

# from .constants import GENDER_CHOICES
# from .managers import UserManager
# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True, null=False, blank=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email

#     @property
#     def balance(self):
#         if hasattr(self, 'account'):
#             return self.account.balance
#         return 0


# class BankAccountType(models.Model):
#     name = models.CharField(max_length=128)
#     maximum_withdrawal_amount = models.DecimalField(
#         decimal_places=2,
#         max_digits=12
#     )
#     def __str__(self):
#         return self.name


# class UserBankAccount(models.Model):
#     user = models.OneToOneField(
#         User,
#         related_name='account',
#         on_delete=models.CASCADE,
#     )
#     account_type = models.ForeignKey(
#         BankAccountType,
#         related_name='accounts',
#         on_delete=models.CASCADE
#     )
#     account_no = models.PositiveIntegerField(unique=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     birth_date = models.DateField(null=True, blank=True)
#     balance = models.DecimalField(
#         default=0,
#         max_digits=12,
#         decimal_places=2
#     )
#     initial_deposit_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return str(self.account_no)



# class UserAddress(models.Model):
#     user = models.OneToOneField(
#         User,
#         related_name='address',
#         on_delete=models.CASCADE,
#     )
#     street_address = models.CharField(max_length=512)
#     city = models.CharField(max_length=256)
#     postal_code = models.PositiveIntegerField()
#     country = models.CharField(max_length=256)

#     def __str__(self):
#         return self.user.email

        
        
        
        
        
        
        
        
        
        
        
