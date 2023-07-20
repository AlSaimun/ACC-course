
import datetime 
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm): 
        class Meta: 
                model = Transaction
                fields = ['amount', 'transaction_type']
        
        # if we do not want to show transaction_type, then it is not necessary 
        def __init__(self, *args, **kwargs): 
                self.account = kwargs.pop('account')
                super().__init__(*args, **kwargs)
                self.fields['transaction_type'].disabled = True # we can also make it enabled to show it 
                self.fields['transaction_type'].widget = forms.HiddenInput()
                
        def save(self, commit=True): 
                self.instance.account = self.account
                self.instance.balance_after_transaction = self.account.balance 
                return super().save()
        
class DepositForm(TransactionForm): 
        def clean_amount(self): 
                # min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT
                min_deposit_amount = 500 
                amount = self.cleaned_data.get('amount')
                
                if amount < min_deposit_amount: 
                        raise forms.ValidationError(
                                f'You need to deposit at least $ {min_deposit_amount}'
                        )
                return amount 


class WithdrawForm(TransactionForm): 
        def clean_amount(self): 
                account = self.account
                min_withdraw_amount = 500 
                max_withdrawl_amount = (
                        account.account_type.maximum_withdrawl_amount
                )
                balance = account.balance
                amount = self.cleaned_data.get('amount')
                if amount < min_withdraw_amount: 
                        raise forms.ValidationError(
                                f'You must withdraw at least $ {min_withdraw_amount}'
                        )
                
                if amount > max_withdrawl_amount: 
                        raise forms.ValidationError(
                                f'You can withdraw at most $ {max_withdrawl_amount}'
                        )
                
                if amount > balance: 
                        raise forms.ValidationError(
                                f'Insufficient balance!'
                                f'You have $ {balance} in your bank account'
                        )
                
                return amount 
                
class LoanRequestForm(TransactionForm): 
        def clean_amount(self): 
                amount = self.cleaned_data.get('amount')
                return amount 
                
                
                
        

