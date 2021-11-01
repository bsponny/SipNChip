from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect

from SipNChipApp.decorators import allowed_user_types, unauthenticated_user
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Tournament, SponsorRequest, Account
from datetime import date


from django.contrib.auth.decorators import login_required

@login_required(login_url='SipNChipApp:login')
# @allowed_user_types(allowed_types=[4])
def userType(request):
    accounts = Account.objects.order_by('user')
    context = {
            'accounts': accounts,
            }
    return render(request, 'SipNChipApp/userType.html', context)

@login_required(login_url='SipNChipApp:login')
# @allowed_user_types(allowed_types=[4])
def setUserType(request):
    username = request.POST.get('username')
    userType = request.POST.get('userType')
    user = get_object_or_404(User, username=username)
    account = get_object_or_404(Account, user=user)
    account.userType = userType
    account.save()
    return HttpResponseRedirect('/userType')

@login_required(login_url='SipNChipApp:login')
def home(request):
    if request.user.account.userType == 1:
        userType = 'player'
    elif request.user.account.userType == 2:
        userType = 'sponsor'
    elif request.user.account.userType == 3:
        userType = 'bartender'
    elif request.user.account.userType == 4:
        userType = 'manager'
    context = {
        'userType': userType,
        'balance': request.user.account.balance,
        'username': request.user,
    }
    return render(request, 'SipNChipApp/home.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)

            user = User.objects.get(username=username)

            balance = user.account.balance
            messages.success(request, 'Current account balance is $' + str(balance))

            userType = user.account.userType
            userTypeName = ""
            if userType == 1:
                userTypeName = "Player"
            elif userType == 2:
                userTypeName = "Sponsor"
            elif userType == 3:
                userTypeName = "Bartender"
            else:
                userTypeName = "Manager"
            messages.success(request, "Current user type is a " + userTypeName)

            return redirect('SipNChipApp:login')

    context = {'form': form}
    return render(request, 'SipNChipApp/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('SipNChipApp:home')
        else:
            messages.info(request, 'Username or password is incorrect.')

    return render(request, 'SipNChipApp/login.html', {})

@login_required(login_url='SipNChipApp:login')
def logoutUser(request):
    logout(request)
    return redirect('SipNChipApp:login')

@login_required(login_url='SipNChipApp:login')
# @allowed_user_types(allowed_types=[4])
def tournamentCreation(request):
    message = ""
    
    if request.method == 'POST':
        dayOfTournament = request.POST['dayOfTournament']
        if date.fromisoformat(dayOfTournament) < date.today():
            message = "Error: Cannot create tournament on a past date"
            return render(request, 'SipNChipApp/tournament-creation.html', {'message': message})
        tournament = Tournament()
        tournament.dayOfTournament = dayOfTournament
        tournament.save()
        message = "Tournament was created for " + request.POST['dayOfTournament']

    return render(request, 'SipNChipApp/tournament-creation.html', {'message': message})

@login_required(login_url='SipNChipApp:login')
def tournaments(request):
    tournament_list = Tournament.objects.filter(dayOfTournament__gte=date.today())
    tournament_list = tournament_list.order_by('dayOfTournament')
    if tournament_list.count() == 0:
        messages.info(request, "There are currently no tournaments available to register for")
    context = {'tournament_list': tournament_list}
    return render(request, 'SipNChipApp/tournaments.html', context)

@login_required(login_url='SipNChipApp:login')
def archivedTournaments(request):
    userType = request.user.account.userType
    if userType == 4:
        archive = Tournament.objects.filter(dayOfTournament__lt=date.today())
    else:
        archive = Tournament.objects.filter(dayOfTournament__lt=date.today(), playersRegistered=request.user)
    if archive.count() == 0:
        messages.info(request, "There are currently no archived tournaments")
    context = {'archive': archive}
    return render(request, 'SipNChipApp/archived-tournaments.html', context)

@login_required(login_url='SipNChipApp:login')
def signup(request):
    id = request.POST.get('id')
    tournament = get_object_or_404(Tournament, pk=id)
    tournament.playersRegistered.add(request.user)
    tournament.save()
    messages.success(request, f"Successfully signed up for tournament on {tournament.dayOfTournament}")
    return HttpResponseRedirect('/tournaments')

@login_required(login_url='SipNChipApp:login')
# @allowed_user_types(allowed_types=[2])
def requestTournament(request):
    if request.method == "POST":
        dayOfTournament = request.POST.get("date")
        if date.fromisoformat(dayOfTournament) < date.today():
            messages.error(request, "Error: Cannot create tournament on a past date")
            return render(request, 'SipNChipApp/request-tournament.html', {})
        sponsorRequest = SponsorRequest(sponsor=request.user, dayOfTournament=dayOfTournament)
        sponsorRequest.save()
        messages.success(request, f"Successfully submitted request for tournament on {dayOfTournament}")
    return render(request, 'SipNChipApp/request-tournament.html', {})

@login_required(login_url='SipNChipApp:login')
# @allowed_user_types(allowed_types=[4])
def sponsorRequests(request):
    messages = []

    if request.method == 'POST':
        sponsorRequest = get_object_or_404(SponsorRequest, pk=request.POST.get('id'))
        status = request.POST.get('status')
        if (status == 'approve'):
            tournament = Tournament()
            tournament.dayOfTournament = sponsorRequest.dayOfTournament
            tournament.save()
            tournament.sponsoredBy.add(sponsorRequest.sponsor)
            tournament.save()
            messages.append(f"Request was approved and a tournament was created for {tournament}")
        else:
            messages.append(f"Request was denied for a tournament on {sponsorRequest.dayOfTournament}")
        sponsorRequest.delete()

    requests = SponsorRequest.objects.all()
    if requests.count() == 0:
        messages.append("There are currently no sponsor requests")

    context = {'requests': requests, 'messages': messages}
    return render(request, 'SipNChipApp/sponsor-requests.html', context)

@login_required(login_url='SipNChipApp:login')
def sponsorTournament(request):
    tournament_list = Tournament.objects.all()
    if tournament_list.count() == 0:
        messages.info(request, "There are currently no tournaments available to sponsor. Please go to request tournament page.")
    context = {'tournament_list': tournament_list, 'user': request.user}
    return render(request, 'SipNChipApp/sponsor-tournament.html', context)

@login_required(login_url='SipNChipApp:login')
def sponsorByTournamentId(request):
    id = request.POST.get('id')
    tournament = get_object_or_404(Tournament, pk=id)
    tournament.sponsoredBy.add(request.user)
    tournament.save()
    messages.success(request, f"Successfully sponsored tournament on {tournament.dayOfTournament}")
    return HttpResponseRedirect('/sponsor-tournament')

@login_required(login_url='SipNChipApp:login')
def unSponsorByTournamentId(request):
    id = request.POST.get('id')
    tournament = get_object_or_404(Tournament, pk=id)
    tournament.sponsoredBy.remove(request.user)
    tournament.save()
    messages.success(request, f"Successfully withdrawed sponsorship from tournament on {tournament.dayOfTournament}")
    return HttpResponseRedirect('/sponsor-tournament')
# @allowed_user_types(allowed_types=[4])
def manageTournaments(request):
    messages = []

    if request.method == 'POST':
        tournament = get_object_or_404(Tournament, pk=request.POST.get('id'))
        messages.append(f"Tournament on {tournament} was deleted")
        tournament.delete()

    tournaments = Tournament.objects.all()
    if tournaments.count() == 0:
        messages.append("There are currently no tournaments")

    context = {'tournaments': tournaments, 'messages': messages}
    return render(request, 'SipNChipApp/manage-tournaments.html', context)

@login_required(login_url='SipNChipApp:login')
def userTournaments(request):
    tournament_list = Tournament.objects.filter(dayOfTournament__gte=date.today())
    tournament_list = tournament_list.filter(playersRegistered__exact=request.user)
    tournament_list = tournament_list.order_by('dayOfTournament')
    if tournament_list.count() == 0:
        messages.info(request, "There are currently no tournaments available to register for")
    context = {'tournament_list': tournament_list}
    return render(request, 'SipNChipApp/userTournaments.html', context)

@login_required(login_url='SipNChipApp:login')
def deregister(request):
    id = request.POST.get('id')
    tournament = get_object_or_404(Tournament, pk=id)
    tournament.playersRegistered.remove(request.user)
    tournament.save()
    messages.success(request, f"Successfully deregistered for tournament on {tournament.dayOfTournament}")
    return HttpResponseRedirect('/user-tournaments')
