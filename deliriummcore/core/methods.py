from django.shortcuts import get_object_or_404
from main.methods import getCoreRole
from django.contrib.auth.models import User
from core.models import CoreOrg

def checkCoreOrgAdd(user):
    # Si ya es ORG con PROFILE.ROL y COREORG MODEL
    if hasattr(user, 'coreorg') and getCoreRole(user) == 4:
        return (True, "Este usuario ya es Organizador")
    # Si no tiene COREORG MODEL
    elif not hasattr(user, 'coreorg') and getCoreRole(user) == 4:
        return (True, "ERROR - COREORG no creado")
    # Si no tiene PROFILE.ROL
    elif hasattr(user, 'coreorg') and not getCoreRole(user) == 4:
        return (True, "ERROR - ROL no cambiado")
    else:
        return (False, None)

def getCoreOrgAccount(account):
    return CoreOrg.objects.get(account=account)

def getCoreOrgID(id):
    return CoreOrg.objects.get(id=id)



def checkCoreOrgUser(user):
    # Si ya es ORG con PROFILE.ROL y COREORG MODEL
    if hasattr(user, 'coreorg') and getCoreRole(user) == 4:
        return (True, None)
    # Si no tiene COREORG MODEL
    elif not hasattr(user, 'coreorg') and getCoreRole(user) == 4:
        return (False, "ERROR - COREORG no creado")
    # Si no tiene PROFILE.ROL
    elif hasattr(user, 'coreorg') and not getCoreRole(user) == 4:
        return (False, "ERROR - ROL no cambiado")
    else:
        return (False, "ERROR ?")