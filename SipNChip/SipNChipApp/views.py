from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect

from SipNChipApp.decorators import allowed_user_types, unauthenticated_user
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import DrinkOrder, Tournament, SponsorRequest, Account, Scorecard, Drink, OrderNotification
from datetime import date
from decimal import Context, Decimal


from django.contrib.auth.decorators import login_required

@login_required(login_url='SipNChipApp:login')
# @allowed_user_types(allowed_types=[4])
def userType(request):
    accounts = Account.objects.order_by('user').exclude(userType=5)
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
    adminAccount = get_object_or_404(Account, userType=5)
    if request.user.account.userType == 1:
        userType = 'player'
    elif request.user.account.userType == 2:
        userType = 'sponsor'
    elif request.user.account.userType == 3:
        userType = 'bartender'
    elif request.user.account.userType == 4:
        userType = 'manager'
    elif request.user.account.userType == 5:
        userType = 'admin'
    context = {
        'userType': userType,
        'balance': request.user.account.balance,
        'companyBalance': adminAccount.balance,
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
            elif userType == 4:
                userTypeName = "Manager"
            elif userType == 5:
                userTypeName = "Administrator"
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
        archive = archive.order_by('dayOfTournament')
    else:
        archive = Tournament.objects.filter(dayOfTournament__lt=date.today(), playersRegistered=request.user)
        archive = archive.order_by('dayOfTournament')
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
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        dayOfTournament = request.POST.get("date")
        if date.fromisoformat(dayOfTournament) < date.today():
            messages.error(request, "Error: Cannot create tournament on a past date")
            return render(request, 'SipNChipApp/request-tournament.html', {})
        if account.balance >= 500:
            account.balance -= 500
            account.save()
            sponsorRequest = SponsorRequest(sponsor=request.user, dayOfTournament=dayOfTournament)
            sponsorRequest.save()
            messages.success(request, f"Successfully submitted request for tournament on {dayOfTournament}")
        else:
            account.triedToSponsor = True
            account.save()
            return HttpResponseRedirect('/balance')
    return render(request, 'SipNChipApp/request-tournament.html', {})

@login_required(login_url='SipNChipApp:login')
# @allowed_user_types(allowed_types=[4])
def sponsorRequests(request):
    messages = []

    if request.method == 'POST':
        sponsorRequest = get_object_or_404(SponsorRequest, pk=request.POST.get('id'))
        sponsorAccount = get_object_or_404(Account, user=sponsorRequest.sponsor)
        adminAccount = get_object_or_404(Account, userType=5)
        status = request.POST.get('status')
        if (status == 'approve'):
            tournament = Tournament()
            tournament.dayOfTournament = sponsorRequest.dayOfTournament
            tournament.save()
            tournament.sponsoredBy.add(sponsorRequest.sponsor)
            tournament.save()
            adminAccount.balance += 500
            adminAccount.save()

            messages.append(f"Request was approved and a tournament was created for {tournament}")
        else:
            messages.append(f"Request was denied for a tournament on {sponsorRequest.dayOfTournament}")
            sponsorAccount.balance += 500
            sponsorAccount.save()
        sponsorRequest.delete()

    requests = SponsorRequest.objects.all()
    requests = requests.order_by('dayOfTournament')
    if requests.count() == 0:
        messages.append("There are currently no sponsor requests")

    context = {'requests': requests, 'messages': messages}
    return render(request, 'SipNChipApp/sponsor-requests.html', context)

@login_required(login_url='SipNChipApp:login')
def sponsorTournament(request):
    tournament_list = Tournament.objects.all()
    tournament_list = tournament_list.order_by('dayOfTournament')
    if tournament_list.count() == 0:
        messages.info(request, "There are currently no tournaments available to sponsor. Please go to request tournament page.")
    context = {'tournament_list': tournament_list, 'user': request.user}
    return render(request, 'SipNChipApp/sponsor-tournament.html', context)

@login_required(login_url='SipNChipApp:login')
def sponsorByTournamentId(request):
    account = get_object_or_404(Account, user=request.user)
    adminAccount = get_object_or_404(Account, userType=5)
    if account.balance >= 500:
        id = request.POST.get('id')
        tournament = get_object_or_404(Tournament, pk=id)
        tournament.sponsoredBy.add(request.user)
        tournament.save()
        account.balance -= 500
        account.save()
        adminAccount.balance += 500
        adminAccount.save()
        messages.success(request, f"Successfully sponsored tournament on {tournament.dayOfTournament}")
    else:
        account.triedToSponsor = True
        account.save()
        return HttpResponseRedirect('/balance')
    return HttpResponseRedirect('/sponsor-tournament')

@login_required(login_url='SipNChipApp:login')
def unSponsorByTournamentId(request):
    account = get_object_or_404(Account, user=request.user)
    adminAccount = get_object_or_404(Account, userType=5)
    id = request.POST.get('id')
    tournament = get_object_or_404(Tournament, pk=id)
    tournament.sponsoredBy.remove(request.user)
    tournament.save()
    account.balance += 500
    account.save()
    adminAccount.balance -= 500
    adminAccount.save()
    messages.success(request, f"Successfully withdrew sponsorship from tournament on {tournament.dayOfTournament}")
    return HttpResponseRedirect('/sponsor-tournament')

# @allowed_user_types(allowed_types=[4])
def manageTournaments(request):
    messages = []

    if request.method == 'POST':
        tournament = get_object_or_404(Tournament, pk=request.POST.get('id'))
        adminAccount = get_object_or_404(Account, userType=5)
        sponsorList = tournament.sponsoredBy.all()
        if len(sponsorList) > 0:
            sponsor = sponsorList[0]
            sponsorAccount = get_object_or_404(Account, user=sponsor)
            sponsorAccount.balance += 500
            sponsorAccount.save()
            adminAccount.balance -= 500
            adminAccount.save()
            messages.append(f"{sponsor} was refunded $500")
        messages.append(f"Tournament on {tournament} was deleted")
        tournament.delete()

    tournaments = Tournament.objects.all()
    tournaments = tournaments.order_by("dayOfTournament")
    if tournaments.count() == 0:
        messages.append("There are currently no tournaments")

    context = {'tournaments': tournaments, 'messages': messages}
    return render(request, 'SipNChipApp/manage-tournaments.html', context)

@login_required(login_url="SipNChipApp:login")
def scorecard(request, tournament_id, hole):
    player = request.user
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if player not in tournament.playersRegistered.all():
        messages.error(request, "Error: You are not registered for that tournament. Please sign up for it first.")
        return HttpResponseRedirect('/tournaments/')
    try:  # tests if a score already exists in the leaderboard for the user
        tournament.leaderboard[player.username]
        messages.error(request, "Error: You have already submitted your scores for this tournament.")
        return HttpResponseRedirect("/tournaments/")
    except KeyError:
        pass
    if hole < 1 or hole > 18:
        return HttpResponseRedirect("/tournaments/")

    scorecard = Scorecard.objects.filter(player=player, tournament=tournament)
    if scorecard.count() > 1:
        messages.error(request, "Error: More than one scorecard exists for this player/tournament combo somehow.")
        return HttpResponseRedirect('/tournaments/')  # return to registered tournaments page
    elif scorecard.count() == 0:
        scorecard = Scorecard(player=player, tournament=tournament)
        scorecard.save()
        player.account.currentHole = 1
        player.save()
    else:
        scorecard = scorecard.get(player=player)

    currentHole = player.account.currentHole
    if hole > currentHole:
        messages.error(request, f"Error: You cannot submit scores for holes you haven't played yet. You are currently "
                                f"at hole {currentHole}.")
        return HttpResponseRedirect(f'/scorecard/{tournament_id}/{currentHole}')


    if request.method == 'POST':
        currentScore = request.POST.get('currentScore')
        if int(currentScore) < 1 or int(currentScore) > 5:
            messages.error(request, "Error: Invalid score entered. Please enter a score between 1 and 5.")
            return HttpResponseRedirect(f'/scorecard/{tournament_id}/{currentHole}')
        scorecard.scores[hole] = currentScore
        scorecard.save()
        messages.success(request, "Score saved")
        if hole == currentHole and currentHole < 18:
            currentHole += 1
        player.account.currentHole = currentHole
        player.save()

    context = {'scorecard': scorecard, 'hole': hole, 'tournament_id': tournament_id}

    return render(request, 'SipNChipApp/scorecard.html', context)

@login_required(login_url="SipNChipApp:login")
def summary(request, tournament_id):
    player = request.user
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if player not in tournament.playersRegistered.all():
        messages.error(request, "Error: You are not registered for that tournament. Please sign up for it first.")
        return HttpResponseRedirect('/tournaments/')

    scorecard = Scorecard.objects.get(player=player, tournament=tournament)
    scores = scorecard.scores.values()
    totalScore = 0
    for score in scores:
        totalScore += int(score)

    if request.method == "POST":
        tournament.leaderboard[str(request.user)] = totalScore
        tournament.save()
        messages.success(request, "Successfully submitted your scores. Congratulations!")
        return HttpResponseRedirect(f"/leaderboard/{tournament_id}")

    context = {'scorecard': scorecard,
               'current_hole': player.account.currentHole,
               'total_score': totalScore,
               'tournament_id': tournament_id}

    return render(request, 'SipNChipApp/summary.html', context)

@login_required(login_url="SipNChipApp:login")
def leaderboard(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    playerObjects = tournament.playersRegistered.all()
    unsortedPlayers = []
    for player in playerObjects:
        try:
            unsortedPlayers.append([str(player), tournament.leaderboard[str(player)]])
        except KeyError:
            pass
    userType = request.user.account.userType
    isOpen = tournament.isOpen
    
    players = sorted(unsortedPlayers, key=lambda player: player[1])
    context = {'tournament': tournament, 'players': players, 'userType': userType, 'isOpen': isOpen,}
    return render(request, 'SipNChipApp/leaderboard.html', context)

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

@login_required(login_url='SipNChipApp:login')
def balance(request):
    username = request.user
    balance = request.user.account.balance
    triedToSponsor = request.user.account.triedToSponsor
    message = ""
    if balance < 500 and triedToSponsor:
        remainder = 500 - balance
        message = "You need $500 to sponsor a tournament. Please add $" + str(remainder) + " to your account."
        request.user.account.triedToSponsor = False
        request.user.account.save()
    context = {
            'username': username,
            'balance': balance,
            'message': message,
            }
    return render(request, 'SipNChipApp/balance.html', context)

@login_required(login_url='SipNChipApp:login')
def addMoney(request):
    amount = request.POST.get('amount')
    if amount != "":
        amount = Decimal(amount)
        if amount < 0:
            messages.error(request, "You can't add a negative amount of money.")
            return HttpResponseRedirect('/balance')
        else:
            account = get_object_or_404(Account, user=request.user)
            account.balance += amount
            account.save()
            return HttpResponseRedirect('/balance')
    else:
        messages.error(request, "Please specify how much money to add")
        return HttpResponseRedirect('/balance')

@login_required(login_url='SipNChipApp:login')
def drinkMenu(request):
    if request.method == "POST":
        drinkId = request.POST.get('drink-id')
        drink = get_object_or_404(Drink, pk=drinkId)
        drink.delete()

    drinks = Drink.objects.all()
    if drinks.count() == 0:
        messages.info(request, "There are currently no drinks available")
    context = {'drinks': drinks}

    return render(request, 'SipNChipApp/drink-menu.html', context)

@login_required(login_url='SipNChipApp:login')
def addDrink(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        drink = Drink(name=name, description=description, price=price)
        drink.save()
        messages.success(request, "Successfully added drink to menu")
        return HttpResponseRedirect('/drink-menu/')

    return render(request, 'SipNChipApp/add-drink.html', {})

@login_required(login_url='SipNChipApp:login')
def editDrink(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)

    if request.method == "POST":
        newName = request.POST.get('name')
        drink.name = newName
        newDescription = request.POST.get('description')
        drink.description = newDescription
        newPrice = request.POST.get('price')
        drink.price = newPrice
        drink.save()
        messages.success(request, f"Successfully edited {newName}")
        return HttpResponseRedirect('/drink-menu')

    context = {'drink': drink, 'drink_id': drink_id}

    return render(request, 'SipNChipApp/edit-drink.html', context)

@login_required(login_url='SipNChipApp:login')
# @allowed_user_types(allowed_types=[3, 4, 5])
def drinkOrders(request):
    messages = []

    if request.method == 'POST':
        drinkorder = get_object_or_404(DrinkOrder, pk=request.POST.get('id'))
        messages.append("Drink order for " + str(drinkorder.orderedBy) + " was marked as complete")
        notificationMessage = "Your drink order is ready "
        currentHole = drinkorder.orderedBy.account.currentHole
        delivery = f"and is being delievered to hole {currentHole}" if currentHole > 0 else "and is ready for pickup at the bar"
        notificationMessage += delivery
        notification = OrderNotification(user=drinkorder.orderedBy, message=notificationMessage)
        notification.save()
        drinkorder.delete()

    drinkOrders = DrinkOrder.objects.all()
    if drinkOrders.count() == 0:
        messages.append("There are currently no drink orders")

    context = {'drinkOrders': drinkOrders, 'messages': messages}
    return render(request, 'SipNChipApp/drink-orders.html', context)

def userOrders(request):
    account = get_object_or_404(Account, user=request.user)
    adminAccount = get_object_or_404(Account, userType=5)

    messages = []

    if request.method == 'POST':
        drinkOrder = get_object_or_404(DrinkOrder, pk=request.POST.get('id'))
        messages.append("Drink order totaling " + str(drinkOrder.totalPrice) + " was canceled")
        account.balance += drinkOrder.totalPrice
        account.save()
        adminAccount.balance -= drinkOrder.totalPrice
        adminAccount.save()
        drinkOrder.delete()

    drinkOrders = DrinkOrder.objects.filter(orderedBy__exact=request.user)
    if drinkOrders.count() == 0:
        messages.append("You currently have no drink orders")
    
    context = {'drinkOrders': drinkOrders, 'messages': messages}
    return render(request, 'SipNChipApp/user-orders.html', context)

@login_required(login_url='SipNChipApp:login')
def notifications(request):
    user = request.user
    notifications = OrderNotification.objects.filter(user=user)

    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        notification = OrderNotification.objects.get(id=notification_id)
        notification.delete()
        return HttpResponseRedirect('/notifications')

    if notifications.count() == 0:
        messages.info(request, "You currently have no notifications")

    return render(request, 'SipNChipApp/notifications.html', {'notifications': notifications})

def endTournament(request, tournamentId):
    adminAccount = get_object_or_404(Account, userType=5)
    tournament = get_object_or_404(Tournament, pk=tournamentId)
    leaderboard = tournament.leaderboard
    sortedLeaderboard = sorted(leaderboard.items(), key=lambda x:x[1])

    if len(sortedLeaderboard) > 0:
        firstPlaceUserObject = sortedLeaderboard[0]
        firstPlaceUsername = firstPlaceUserObject[0]
        firstPlaceUser = get_object_or_404(User, username=firstPlaceUsername)
        firstPlaceAccount = get_object_or_404(Account, user=firstPlaceUser)
        firstPlaceAccount.balance += 100
        firstPlaceAccount.save()
        adminAccount.balance -= 100
        adminAccount.save()
        messages.success(request, f"Successfully gave " + firstPlaceUsername + " $100")

    if len(sortedLeaderboard) > 1:
        secondPlaceUserObject = sortedLeaderboard[1]
        secondPlaceUsername = secondPlaceUserObject[0]
        secondPlaceUser = get_object_or_404(User, username=secondPlaceUsername)
        secondPlaceAccount = get_object_or_404(Account, user=secondPlaceUser)
        secondPlaceAccount.balance += 50
        secondPlaceAccount.save()
        adminAccount.balance -= 50
        adminAccount.save()
        messages.success(request, f"Successfully gave " + secondPlaceUsername + " $50")

    if len(sortedLeaderboard) > 2:
        thirdPlaceUserObject = sortedLeaderboard[2]
        thirdPlaceUsername = thirdPlaceUserObject[0]
        thirdPlaceUser = get_object_or_404(User, username=thirdPlaceUsername)
        thirdPlaceAccount = get_object_or_404(Account, user=thirdPlaceUser)
        thirdPlaceAccount.balance += 25
        thirdPlaceAccount.save()
        adminAccount.balance -= 25
        adminAccount.save()
        messages.success(request, f"Successfully gave " + thirdPlaceUsername + " $25")

    tournament.isOpen = False
    tournament.save()

    return HttpResponseRedirect('/leaderboard/'+ str(tournamentId) + '/')

@login_required(login_url='SipNChipApp:login')
def orderDrinks(request):
    account = get_object_or_404(Account, user=request.user)
    adminAccount = get_object_or_404(Account, userType=5)

    messages = []

    if request.method == 'POST':
        total = 0
        order = DrinkOrder()
        order.orderedBy = request.user
        for drink in Drink.objects.all():
            quantity = request.POST.get(str(drink.id))
            if (int(quantity) > 0):
                order.drinks[str(drink)] = quantity
                total += float(quantity) * float(drink.price)
        order.totalPrice = total
        order.save()

        account.balance -= Decimal(total)
        account.save()
        adminAccount.balance -= Decimal(total)
        adminAccount.save()

        messages.append("Successfuly submitted order totaling " + str(order.totalPrice))        

    drinks = Drink.objects.all()

    context = {'drinks': drinks, 'messages': messages}
    return render(request, 'SipNChipApp/order-drinks.html', context)
