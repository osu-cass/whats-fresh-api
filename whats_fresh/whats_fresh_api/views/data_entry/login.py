from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse


def login_user(request):
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

    return HttpResponse('')
