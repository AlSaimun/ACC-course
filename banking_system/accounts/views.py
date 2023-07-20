from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from .forms import UserRegistrationForm, UserAddressForm


User = get_user_model()

class UserRegistrationView(TemplateView): 
        model = User
        form_class = UserRegistrationForm
        template_name = 'accounts/user_registration.html'
        
        def dispathch(self, request, *args, **kwargs): 
                if self.request.user.is_authenticated: 
                        return HttpResponseRedirect(
                                reverse_lazy('transactions:transaction_report')
                        ) 
                return super().dispatch(request, *args, **kwargs)
        
        def post(self, request, *args, **kwargs): 
                registration_form = UserRegistrationForm(self.request.POST)
                address_from = UserAddressForm(self.request.POST)
                
                if registration_form.is_valid() and address_from.is_valid(): 
                        user = registration_form.save()
                        address = address_from.save(commit=False)
                        address.user = user
                        address.save()
                        
                        login(self.request, user)
                        messages.success(self.request, 
                                (
                                        f'Thank You For Creating Account In Our Bank'
                                        f'Your Account Number is {user.account.account_no}'
                                )
                        )
                        
                        return HttpResponseRedirect(
                                reverse_lazy('transactions:deposit_money')
                        )

                # normal get | showing the form the user before the post request 
                return self.render_to_response(
                        self.get_context_data(
                                registration_form=registration_form, 
                                address_from=address_from
                        )
                )
                
        def get_context_data(self, **kwargs): 
                # for the first time, the user is visiting the page, the kwargs is an empty dict. in that case, passing the forms 
                if 'registration_form' not in kwargs: 
                        kwargs['registration_form'] = UserRegistrationForm()
                
                if 'address_form' not in kwargs: 
                        kwargs['address_form'] = UserAddressForm()
                        
                return super().get_context_data(**kwargs)
                
                
class UserLoginView(LoginView): 
        ''' user log in  '''
        template_name='accounts/user_login.html'
        redirect_authenticated_user = False 
        
class UserLogoutView(RedirectView): 
        ''' user log out  '''
        pattern_name = 'home'
        def get_redirect_url(self, *args, **kwargs): 
                if self.request.user.is_authenticated: 
                        logout(self.request)
                return super().get_redirect_url(*args, **kwargs)
                
                
                
                
                
                
                
                
                
                
                