from django.shortcuts import render,redirect
from .models import CustomSetPasswordForm
from .forms import SingUpForm,ChagneUserData
from django.contrib import messages 
from book_management.views import BookSearchForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request,'user_authentication/home.html',{'name':request.user})
    else:
        return render(request,'user_authentication/home.html')
    
    
def about(request):
    if request.user.is_authenticated:
        return render(request,'user_authentication/about.html')
    else:
        return render(request,'user_authentication/about.html')
    
    
def rule(request):
    if request.user.is_authenticated:
        return render(request,'user_authentication/rule.html')
    else:
        return render(request,'user_authentication/rule.html')
        

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SingUpForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Your account has been created successfully')
                form.save()
                return redirect('profile')
        else : 
            form = SingUpForm()
        template_path = 'user_authentication/signup.html'
        return render(request, template_path, {'form' : form})
    else:    
        return render(request,'user_authentication/home.html',{'name':request.user_name,'form':form})
    
    
def user_login(request):
    if request.user.is_authenticated:
        return render(request,'user_authentication/profile.html',{'name':request.user}) 
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data = request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pas = form.cleaned_data['password']
            user = authenticate(username=user_name,password = user_pas)
            if user is not None:
                login(request,user)
                print('success')
                messages.success(request,'Log in successfully')
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request,'user_authentication/login.html',{'form':form})
            
            
            
def profile(request):
    if request.user.is_authenticated:
        return render(request,'user_authentication/profile.html',{'name':request.user}) 
    else:
        return redirect('login')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')
    
def change_user(request):
    if request.method == 'POST':
        form = ChagneUserData(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.warning(request,'Update Successfully')
            return redirect('profile')
    else:
        form = ChagneUserData(instance=request.user)
    print('from',form)
    return render(request, 'user_authentication/update_data.html', {'form': form})


def change_password(request): 
    if not request.user.is_authenticated: 
        return redirect('login')
    if request.method == 'POST': 
        form = CustomSetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid(): 
            form.save()
            messages.warning(request,'Successfully changed your password')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else: 
            form = CustomSetPasswordForm(user=request.user)
        return render(request,'user_authentication/change_pass.html', {'form' : form})
    else:
        form = CustomSetPasswordForm(user=request.user)
        return render(request,'user_authentication/change_pass.html', {'form' : form})


