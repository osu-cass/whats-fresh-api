from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def login_user(request):
    """
    */login*

    This view will display a login page if GET'd, or attempt login if POST'd.
    If the GET parameter logout is set, it will change the message on the page
    to indicate a successful logout.

    If a user is already logged in and tries to access this page, they will be
    redirected to /entry.
    """
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST.get('next'):
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return HttpResponseRedirect('/entry')
            else:
                state = "Your account is not active."
        else:
            next = request.POST.get('next')
            state = "Invalid username or password."
    else:
        next = request.GET.get('next')

    if request.GET.get('logout', False):
        state = "Logged out successfully!"

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'auth.html', {
        'state': state, 'username': username, 'next': next, 'title': 'Log In'})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('{}?logout=true'.format(reverse('login')))


def root(request):
    """
    This function handles /. At the current time, / redirects to /login,
    which may redirect to /entry if the user is already logged in.
    """
    return HttpResponseRedirect(reverse('login'))
