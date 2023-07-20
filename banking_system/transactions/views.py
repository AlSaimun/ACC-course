from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, View
from datetime import datetime
from django.db.models import Sum

from transactions.forms import DepositForm, WithdrawForm, LoanRequestForm, TransactionForm
from transactions.constants import DEPOSIT, WITHDRAWL, LOAN_REQUEST, LOAN_REPAY
from transactions.models import Transaction



class TransactionReportView(LoginRequiredMixin, ListView): 
        template_name = 'transactions/transaction_report.html'
        model = Transaction
        form_data = {}
        balance = 0 
        # def get(self, request, *args, **kwargs): 
        #         form = TransactionDateRangeForm(request.GET or None)
        #         if form.is_valid(): 
        #                 self.form_data = form.cleaned_data
        #         return super().get(request, *args, **kwargs)

        def get_queryset(self): 
                queryset = super().get_queryset().filter(account=self.request.user.account)
                start_date_str = self.request.GET.get('start_date')
                end_date_str = self.request.GET.get('end_date')
                
                if start_date_str and end_date_str: 
                        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                        end_date = datetime.strptime(end_date_str,  '%Y-%m-%d').date()
                        queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
                        self.balance = Transaction.objects.filter(
                                timestamp__date__gte=start_date, timestamp__date__lte=end_date
                        ).aaggregate(Sum('amount'))['amount__sum']
                
                else: 
                        self.balance = self.request.user.account.balance
                
                return queryset.distinct()
        
        # normal get | initial showing to the user 
        def get_context_data(self, **kwargs): 
                context = super().get_context_data(**kwargs)
                context.update({
                        'account' : self.request.user.account, 
                })        
        
                return context 
        
        

class TransactionCreateMixin(LoginRequiredMixin, CreateView): 
        template_name = 'transactions/transaction_form.html'
        model = Transaction
        title = ''
        success_url = reverse_lazy('transactions:transaction_report')
        # success_url = reverse_lazy('/transactions/transaction_report/')
        
        # def get_form_kwargs(self): 
        #         kwargs = super().get_forms_kwargs()
        #         kwargs.update({
        #                 'account' : self.request.user.account
        #         })
        #         return kwargs
        def get_form_kwargs(self):
                kwargs = super().get_form_kwargs()
                kwargs.update({
                'account': self.request.user.account
                })
                return kwargs

        def get_context_data(self, **kwargs): 
                context = super().get_context_data(**kwargs)
                context.update({
                        'title' : self.title
                })
                
                return context 
        
class DepositMoneyView(TransactionCreateMixin): 
        form_class = DepositForm
        title = 'Deposit Money'
        
        def get_initial(self): 
                initial = {'transaction_type' : DEPOSIT}
                return initial
        
        def form_valid(self, form): 
                amount = form.cleaned_data.get('amount')
                account = self.request.user.account
                
                if not account.initial_deposite_date: 
                        now = timezone.now()
                        account.initial_deposit_date = now 
                account.balance += amount
                account.save(
                        update_fields=[
                                'initial_deposite_date', 
                                'balance',
                        ]
                )

                messages.success(
                        self.request, 
                        f'{"$ {:,.2f}".format(float(amount))} was deposited to your account successfully! '
                )
        
                return super().form_valid(form)
        
        
class WithdrawMoneyView(TransactionCreateMixin): 
        form_class = WithdrawForm
        title = 'Withdraw Money'
        
        def get_initial(self): 
                initial = {'transaction_type' : WITHDRAWL}
                return initial
        
        def form_valid(self, form): 
                amount = form.cleaned_data.get('amount')
                self.request.user.account.balance -= amount
                # account = self.request.user.account
                self.request.user.account.save(update_fields=['balance'])
                

                messages.success(
                        self.request, 
                        f'{" Successfully withdrawn $ {:,.2f}".format(float(amount))} from your account! '
                )
        
                return super().form_valid(form)

class LoanRequestView(TransactionCreateMixin): 
        form_class = LoanRequestForm
        title = 'Request For Loan'
        
        def get_initial(self): 
                initial = {'transaction_type' : LOAN_REQUEST}
                return initial
        
        
        def form_valid(self, form): 
                amount = form.cleaned_data.get('amount')
                current_loan_count = Transaction.objects.filter(
                        account=self.request.user.account, transaction_type=3, loan_approved=True
                ).count()
                
                if current_loan_count >= 3: 
                        return HttpResponse('You have crossed the loan limits of 3')
                
                messages.success(
                        self.request, 
                        f'{" Loan request for $ {:,.2f}".format(float(amount))} submitted successfully! '
                )
                
                return super().form_valid(form)
        

class PayLoanView(LoginRequiredMixin, View): 
        ''' view for loan repay '''
        def get(self, request, loan_id): 
                loan = get_list_or_404(Transaction, id=loan_id)
                # print(loan)
                if loan.loan_approved: 
                        user_account = loan.account 
                        # reduce the loan amount form the user's balance 
                        if loan.amount <= user_account.balance: 
                                user_account.balance -= loan.amount 
                                loan.balance_after_transaction = user_account.balance
                                user_account.save()
                                loan.loan_approved = True 
                                loan.transaction_type = LOAN_REPAY
                                loan.save()
                                return redirect('transactions : loan_list')
                        else: 
                                messages.error(
                                        self.request, 
                                        f'Loan amount is greater than your account balance'
                                )
                return redirect('transactions : loan_list')
        


class LoanListView(LoginRequiredMixin, ListView):
        model = Transaction
        template_name = 'transactions/loan_request.html'
        context_object_name = 'loans'
        
        def get_queryset(self): 
                user_account = self.request.user.account 
                queryset = Transaction.objects.filter(account=user_account, transaction_type=3)
                # print(queryset)
                return queryset
        
        
        
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
        
        

        
        
        
        
        