from django.urls import path
from . import views

urlpatterns = [
    path('userType/', views.userType, name='userType'),
    path('setUserType/', views.setUserType, name='setUserType'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),
    path('tournament-creation/', views.tournamentCreation, name='tournament-creation'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('signup/', views.signup, name='signup'),
    path('request-tournament/', views.requestTournament, name='request-tournament'),
    path('sponsor-requests/', views.sponsorRequests, name='sponsor-requests'),
    path('archived-tournaments', views.archivedTournaments, name='archived-tournaments'),
    path('sponsor-tournament/', views.sponsorTournament, name='sponsor-tournament'),
    path('sponsor-by-tournament-id/', views.sponsorByTournamentId, name='sponsor-by-tournament-id'),
    path('unsponsor-by-tournament-id/', views.unSponsorByTournamentId, name='unsponsor-by-tournament-id'),
    path('manage-tournaments/', views.manageTournaments, name='manage-tournaments'),
    path('user-tournaments/', views.userTournaments, name='user-tournaments'),
    path('deregister/', views.deregister, name='deregister'),
    path('balance/', views.balance, name='balance'),
    path('addMoney/', views.addMoney, name='addMoney'),
]

app_name='SipNChipApp'
