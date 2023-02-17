from django.shortcuts import redirect
from django.contrib import messages


def signin_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access")
            return redirect("signin")
        else:
            return function(request, *args, **kwargs)

    return wrapper
