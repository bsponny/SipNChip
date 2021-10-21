from django.urls import path
from . import views

urlpatterns = [
    path('userType/', views.userType, name='userType'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),
]

app_name='SipNChipApp'
