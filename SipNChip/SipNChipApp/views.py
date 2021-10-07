from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

@login_required(login_url='SipNChipApp:login')
def home(request):
    return render(request, 'SipNChipApp/home.html', {})

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('SipNChipApp:home')
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('SipNChipApp:login')

    context = {'form': form}
    return render(request, 'SipNChipApp/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('SipNChipApp:home')
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

def logoutUser(request):
    logout(request)
    return redirect('SipNChipApp:login')
