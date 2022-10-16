from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Profile
from .methods import checkProfile

# Create your views here.


def landingPage(request):
    if not request.user.is_authenticated:
        return render(request, 'main/landingpage/index.html')
    else:
        return HttpResponseRedirect(reverse("main:home"))


def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    else:
        #Profile Model Creation MEJORAR!!!!!! CON URL UNICA DE CREACIÓN REDIRECT o CAMBIAR SISTEMA DE LOGIN A ANTIGUO Y AVANZADO
        checkProfile(request.user)
        

        #Render home base    
        return render(request, 'main/home.html')


def events(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    else:
        checkProfile(request.user)
        return render(request, 'main/events.html')


def places(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    else:
        checkProfile(request.user)
        return render(request, 'main/places.html')


def wallet(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    else:
        checkProfile(request.user)
        return render(request, 'main/wallet.html')


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    else:
        checkProfile(request.user)
        return render(request, 'main/profile.html')



