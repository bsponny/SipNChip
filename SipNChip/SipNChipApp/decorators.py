from django.shortcuts import redirect

# decorator allowing only unauthenticated users to acces certain pages (login page, register page, etc.)
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('SipNChipApp:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# def allowed_user_types(allowed_types=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
            
#             return view_func(request, *args, **kwargs)
#         return wrapper_func
#     return decorator
