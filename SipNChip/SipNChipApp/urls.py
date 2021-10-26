from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),
    path('tournament-creation/', views.tournamentCreation, name='tournament-creation'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('signup/', views.signup, name='signup'),
    path('request-tournament/', views.requestTournament, name='request-tournament'),
    path('sponsor-requests/', views.sponsorRequests, name='sponsor-requests'),
]

app_name='SipNChipApp'