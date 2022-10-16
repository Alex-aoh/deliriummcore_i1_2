from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),


    #TOOLS
    path("tools/", views.tools, name="tools"),



    #TOOL - 1 - ORGMAIN - INDEX
    path("tools/1/", views.tool_orgmain_index, name="tool_orgmain_index"),
    path("tools/1/lista", views.tool_orgmain_lista, name="tool_orgmain_lista"),
    path("tools/1/add_org", views.tool_orgmain_add_org, name="tool_orgmain_add_org"),

    #TOOL - 2 - BRANDMAIN - INDEX
    path("tools/2/", views.tool_brandmain_index, name="tool_brandmain_index"),





    
]