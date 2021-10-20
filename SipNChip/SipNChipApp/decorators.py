from django.http.response import HttpResponse
from django.shortcuts import redirect

# decorator allowing only unauthenticated users acces to a page (login page, register page, etc.)
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('SipNChipApp:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# decorator allowing only certain user types access to a page
# allowed_types will be a list of numbers corresponding to user types
#     (1=player, 2 = Sponsor, 3 = Bartender, 4 = Manager)
def allowed_user_types(allowed_types=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            type = request.user.account.userType
            if type in allowed_types:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('SipNChipApp:home')
        return wrapper_func
    return decorator
