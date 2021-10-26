from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from SipNChipApp.decorators import allowed_user_types, unauthenticated_user
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Account
from decimal import Decimal

from django.contrib.auth.decorators import login_required

@login_required(login_url='SipNChipApp:login')
def userType(request):
    accounts = Account.objects.order_by('user')
    context = {
            'accounts': accounts,
            }
    return render(request, 'SipNChipApp/userType.html', context)

@login_required(login_url='SipNChipApp:login')
def setUserType(request):
    username = request.POST.get('username')
    userType = request.POST.get('userType')
    user = get_object_or_404(User, username=username)
    account = get_object_or_404(Account, user=user)
    account.userType = userType
    account.save()
    return HttpResponseRedirect(reverse('SipNChipApp:userType'))

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
