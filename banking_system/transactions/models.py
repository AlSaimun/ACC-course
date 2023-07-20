
from django.db import models

from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE_CHOICES


class Transaction(models.Model): 
        account = models.ForeignKey(UserBankAccount, related_name='transactions', on_delete=models.CASCADE)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2)
        loan_approved = models.BooleanField(default=False)
        timestamp = models.DateTimeField(auto_now_add=True)
        transaction_type = models.PositiveIntegerField(choices=TRANSACTION_TYPE_CHOICES)
        
        class Meta: 
                ordering = ['timestamp']