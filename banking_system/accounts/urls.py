
from django.urls import path 
from . import views 

app_name = 'accounts'  

urlpatterns = [
        path('register/', views.UserRegistrationView.as_view(), name='user_registration'),
        path('login/',  views.UserLoginView.as_view(), name='user_login'),
        path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
]
 
