from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.home,name='home'),
   path('about/',views.about,name='about'),
   path('rule/',views.rule,name='rule'),
   path('signup/',views.signup,name='signup'),
   path('profile/',views.profile,name='profile'),
   path('login/',views.user_login,name='login'),
   path('logout/',views.user_logout,name='logout'),
   path('update/',views.change_user,name='update'),
   path('change_pass/',views.change_password,name='change-pass'),
   
]