from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from core.models import CoreTool, CoreOrg, CoreBrand
from core.methods import checkCoreOrgAdd, getCoreOrgAccount, checkCoreOrgUser, getCoreOrgID
from main.methods import checkUser, getUser, checkCoreAccess, getCoreRole, checkCoreToolAccess, changeRole

from main.models import Profile

# CORE MAIN - INDEX PAGE
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        return render(request, 'core/index.html')


# CORE MAIN - DASHBOARD - SEGÚN ROL :)
def dashboard(request):
    # CHECK LOGIN
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # CHECK CORE ACCESS
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))
    
    # CHECKS COMPLETE
    else:
        role = getCoreRole(request.user)

        #If RP
        if role == 2:
            # RP Dashboard render
            return render(request, 'core/admin/admin_dashboard.html', {
                "tools": CoreTool.objects.filter(admin=True),
            })
        #If ADMIN
        elif role == 6:
            # Admin Dashboard render
            return render(request, 'core/admin/admin_dashboard.html', {
                "tools": CoreTool.objects.filter(admin=True),
            })

        #Default Dashboard render
        return render(request, 'core/admin/admin_dashboard.html', {
                "tools": CoreTool.objects.filter(admin=True),
            })


# TOOLS - DEFAULT REDIRECT

def tools(request):
    # CHECK LOGIN
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # CHECK CORE ACCESS
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))
    
    else:
        return HttpResponseRedirect(reverse("core:index"))

#-------------------------#

# Tools - 1 - Administrar Organizadores - #tool_orgmain

# INDEX TOOL
def tool_orgmain_index(request):
    # CHECK LOGIN
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # CHECK CORE ACCESS
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))
    # CHECKS COMPLETE
    else:
        #Check if TOOL Register
        tool = get_object_or_404(CoreTool, name="tool_orgmain")

        #Check TOOL Access
        if checkCoreToolAccess(request.user, tool.id):

            #Default
            return render(request, 'core/tools/orgmain/index.html', {
                "tool": get_object_or_404(CoreTool, id=1),
            })
        #Not Access TOOL
        return HttpResponseRedirect(reverse("main:home"))

# LISTA TOOL
def tool_orgmain_lista(request):
    # CHECK LOGIN
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # CHECK CORE ACCESS
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))
    # CHECKS COMPLETE
    else:
        #Check if TOOL Register
        tool = get_object_or_404(CoreTool, name="tool_orgmain")

        #Check TOOL Access
        if checkCoreToolAccess(request.user, tool.id):

            #Default
            return render(request, 'core/tools/orgmain/org_lista.html', {
                "tool": get_object_or_404(CoreTool, id=1),
                "orgs": CoreOrg.objects.all(),
            })
        #Not Access TOOL
        return HttpResponseRedirect(reverse("main:home"))

# AGREGAR ORGANIZADOR TOOL
def tool_orgmain_add_org(request):
    # CHECK LOGIN
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # CHECK CORE ACCESS
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))
    # CHECKS COMPLETE
    else:
        #Check if TOOL Register
        tool = get_object_or_404(CoreTool, name="tool_orgmain")

        #Check TOOL Access
        if checkCoreToolAccess(request.user, tool.id):

            #POST REQUEST // ADD ORG
            if request.POST:

                #Checar Usuario si existe
                if getUser(str(request.POST["user"])):
                    
                    user = getUser(str(request.POST["user"]))

                    checkOrg = checkCoreOrgAdd(user)
                    if checkOrg[0] == True:
                        return render(request, 'core/tools/orgmain/org_add_org.html', {
                            "tool": get_object_or_404(CoreTool, id=1),
                            "message": checkOrg[1],
                            "message_type": "danger"
                        })
                    
                    name = ""
                    if request.POST["name"] == "":
                        name = "default"
                    else:
                        name = request.POST["name"]
                    # Cambiar Role en PROFILE MODEL
                    changeRole(user, roleint=4)
                
                    # Crear CoreOrg MODEL
                    CoreOrg.objects.create(account=user, name=name)


                    #Return Cambio completo con alerta
                    return render(request, 'core/tools/orgmain/org_add_org.html', {
                        "tool": get_object_or_404(CoreTool, id=1),
                        "message": "Organizador Agregado!",
                        "message_type": "success"
                        })
                # El usuario no existe
                else:
                    #Return usuario no existe con alerta danger
                    return render(request, 'core/tools/orgmain/org_add_org.html', {
                        "tool": get_object_or_404(CoreTool, id=1),
                        "message": "Usuario no encontrado!",
                        "message_type": "danger"
                        })

            #Default
            return render(request, 'core/tools/orgmain/org_add_org.html', {
                "tool": get_object_or_404(CoreTool, id=1),
            })
        #Not Access TOOL
        return HttpResponseRedirect(reverse("main:home"))

#-------------------------#

# Tools - 2 - Administrar Tus Marcas - #tool_brandmain


############# CAMBIAR - VER NOTION

# INDEX TOOL
def tool_brandmain_index(request):
    # CHECK LOGIN
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # CHECK CORE ACCESS
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))
    # CHECKS COMPLETE
    else:
        #Check if TOOL Register
        tool = get_object_or_404(CoreTool, name="tool_brandmain")

        #Check TOOL Access
        if checkCoreToolAccess(request.user, tool.id):
            role = getCoreRole(request.user)
            
            # If Admin ROL 
            if role == 6:
                if request.method == "POST":
                    if request.POST["org"]:
                        org = getCoreOrgID(request.POST["org"])

                        checkOrgUser = checkCoreOrgUser(org.account)
                        #ORG NO PROBLEMS
                        if checkOrgUser[0] == True:
                            return render(request, 'core/tools/brandmain/index.html', {
                                "tool": get_object_or_404(CoreTool, id=2),
                                "brands": CoreBrand.objects.filter(org=getCoreOrgAccount(org.account))
                        })
                    
                        #ORG Problems
                        else:
                            return render(request, 'core/tools/brandmain/index.html', {
                                    "tool": get_object_or_404(CoreTool, id=1),
                                    "message": checkOrgUser[1],
                                    "message_type": "danger"
                                })
                
                return render(request, 'core/tools/brandmain/select_org_admin.html', {
                    "tool": get_object_or_404(CoreTool, id=2),
                    "orgs": CoreOrg.objects.all()
                })

            
            # If Org ROL
            elif role == 4:

                checkOrgUser = checkCoreOrgUser(request.user)
                #ORG NO PROBLEMS
                if checkOrgUser[0] == True:
                    return render(request, 'core/tools/brandmain/index.html', {
                        "tool": get_object_or_404(CoreTool, id=2),
                        "brands": CoreBrand.objects.filter(org=getCoreOrgAccount(request.user))
                })
                
                #ORG Problems
                else:
                    return render(request, 'core/tools/brandmain/index.html', {
                            "tool": get_object_or_404(CoreTool, id=1),
                            "message": checkOrgUser[1],
                            "message_type": "danger"
                        })


            #Default
            return render(request, 'core/tools/brandmain/index.html', {
                "tool": get_object_or_404(CoreTool, id=2),
            })
        #Not Access TOOL
        return HttpResponseRedirect(reverse("main:home"))

#-------------------------#