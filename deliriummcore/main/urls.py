from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path("", views.landingPage, name="landingPage"),
    path("home/", views.home, name="home"),
    path("events/", views.events, name="events"),
    path("wallet/", views.wallet, name="wallet"),
    path("places/", views.places, name="places"),
    path("profile/", views.profile, name="profile"),

]