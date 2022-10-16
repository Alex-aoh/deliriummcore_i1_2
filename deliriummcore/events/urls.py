from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path("<int:requestid>/", views.eventPage, name="eventpage"),
]