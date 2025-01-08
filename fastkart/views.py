from django.shortcuts import render
from django.utils import timezone


def dashboard(request):
    year = timezone.localtime(timezone.now()).strftime('%Y')
    context = {
        'year' : year,
        'link' : "dashboard"
    }
    return render(request, 'backend/dashboard/index.html', context)