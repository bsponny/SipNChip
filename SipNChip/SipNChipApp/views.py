from django.shortcuts import redirect, render
from django.contrib import messages

from SipNChipApp.decorators import unauthenticated_user
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Account
from decimal import Decimal

from django.contrib.auth.decorators import login_required

@login_required(login_url='SipNChipApp:login')
def home(request):
    return render(request, 'SipNChipApp/home.html', {})

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
            account = user.account
            messages.success(request, 'Current account balance is $' + str(account.balance))
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
