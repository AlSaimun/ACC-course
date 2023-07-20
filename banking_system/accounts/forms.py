
from django import forms 
from django.conf import settings 
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction 

from .models import User, BankAccountType, UserBankAccount, UserAddress
from .constants import GENDER_CHOICES 

class UserAddressForm(forms.ModelForm): 
        ''' model form for user address  '''
        class Meta: 
                model = UserAddress 
                exclude = ['user']
                
        def __init__(self, *args, **kwargs): 
                super().__init__(*args, **kwargs)
                ''' some styling '''
                for filed in self.fields: 
                        self.fields[filed].widget.attrs.update({
                                'class' : (
                                        ' appearance-none block w-full bg-gray-200 '
                                        'text-gray-700 border border-gray-200 rounded '
                                        ' py-3 px-4 leading-tight focus: outline-none '
                                        ' focus: bg-white focus: border-gray-500 '
                                )
                        })
                        
class UserRegistrationForm(UserCreationForm): 
        ''' form for user registration  '''
        account_type = forms.ModelChoiceField(queryset=BankAccountType.objects.all())
        gender = forms.ChoiceField(choices=GENDER_CHOICES)
        first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus' : 'on'}))
        last_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus' : 'off'}))
        birth_date = forms.DateField(widget=forms.DateInput(attrs={'type' : 'date'}))
        email = forms.CharField(widget=forms.EmailInput(attrs={'autofocus':'off'}))
        
        class Meta: 
                model = User
                fields = [
                        'first_name',
                        'last_name',
                        'email',
                        'password1',
                        'password2'
                ]
        
        def __init__(self, *args, **kwargs): 
                super().__init__(*args, **kwargs)
                
                for filed in self.fields: 
                        self.fields[filed].widget.attrs.update({
                                'class' : (
                                        ' appearance-none block w-full bg-gray-200 '
                                        'text-gray-700 border border-gray-200 rounded '
                                        ' rounded py-3 px-4 leading-tight leading-tight'
                                        '  focus: outline-none focus: bg-white '
                                        ' focus: border-gray-500 '
                                )
                        })
                        
        # same 
        # def __init__(self, *args, **kwargs):
        #         super().__init__(*args, **kwargs)

        #         for field in self.fields:
        #                 self.fields[field].widget.attrs.update({
        #                         'class': (
        #                         'appearance-none block w-full bg-gray-200 '
        #                         'text-gray-700 border border-gray-200 '
        #                         'rounded py-3 px-4 leading-tight '
        #                         'focus:outline-none focus:bg-white '
        #                         'focus:border-gray-500'
        #                         )
        #                 })
                        

        ''' to save the data automatically '''
        @transaction.atomic
        def save(self, commit=True): 
                user = super().save(commit=False)
                user.set_password(self.cleaned_data.get('password1'))
                
                if commit: 
                        user.save()
                        account_type = self.cleaned_data.get('account_type')
                        gender = self.cleaned_data.get('gender')
                        birth_date = self.cleaned_data.get('birth_date')
                        
                        UserBankAccount.objects.create(
                                user=user, 
                                gender=gender, 
                                birth_date=birth_date, 
                                account_type=account_type, 
                                account_no = (user.id + 100000)
                        )
                
                return user 