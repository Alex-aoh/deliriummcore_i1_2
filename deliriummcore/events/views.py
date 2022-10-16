from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def eventPage(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    else:
        return render(request, 'events/eventpage.html', {
            "requestid": requestid
        })

