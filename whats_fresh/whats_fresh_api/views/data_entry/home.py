from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from whats_fresh.whats_fresh_api.functions import group_required

@login_required
@group_required('Administration Users', 'Data Entry Users')
def home(request):
    return render(request, 'entry.html')
