from django.urls import path

from . import views

app_name = 'oldcore'

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("a/", views.admin_index, name="admin_index"),
    path("a/lista_requests/", views.admin_lista_requests, name="admin_lista_requests"),
    path("a/rp_check/select", views.rp_check_select, name="rp_check_select"),
    path("a/rp_check/<str:username>", views.rp_check_main, name="rp_check_main"),
    path("a/cash/", views.cash_index, name="cash_index"),
    path("a/cash/cashpaytoggle/<int:id>", views.cashpaytoggle, name="cashpaytoggle"),

    path('a/log_websocket/<str:room_name>/', views.log_websocket, name='log_websocket'),

    path("r/new/", views.create_request, name="create_request"),
    path("r/new/create", views.new_ticket_request, name="new_ticket_request"),
    path("r/<int:requestid>", views.request_view, name="request_view"),

    path("r/my_requests", views.my_requests, name="my_requests"),
    path("r/my_requests/list", views.lista_requests, name="lista_requests"),

    path("r/<int:requestid>/delete", views.delete_ticket_request, name="delete_ticket_request"),
    path("a/<int:requestid>", views.admin_request_view, name="admin_request_view"),
    path("a/<int:requestid>/ap", views.aprobar_request, name="aprobar_request"),
    path("a/<int:requestid>/re", views.rechazar_request, name="rechazar_request"),
    path("a/<int:requestid>/ar", views.archivar_request, name="archivar_request"),
    path("a/<int:requestid>/as", views.asignar_request, name="asignar_request"),
    path("t/export/<str:hash>", views.temp_ticket_export, name="temp_ticket_export"),
    path("t/requestall/<str:requestid>", views.image_tickets, name="image_tickets"),
    path("t/image/<str:hash>", views.image_ticket, name="image_ticket"),
    path("t/download/<str:tickethash>", views.download_ticket, name="download_ticket"),
]