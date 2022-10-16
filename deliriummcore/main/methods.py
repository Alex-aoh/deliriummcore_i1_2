from django.shortcuts import get_object_or_404
from .models import Profile
from core.models import CoreTool
from django.contrib.auth.models import User

def checkUser(user):
    if User.objects.filter(username=user):
        return True
    else:
        return False

def getUser(user):
    if checkUser(user):
        return get_object_or_404(User, username=user)
    

def checkProfile(user):
    if not Profile.objects.filter(user=user):
            Profile.objects.create(user=user)

def getProfile(user):
    checkProfile(user)
    return get_object_or_404(Profile, user=user)


def checkCoreAccess(user):
    checkProfile(user)
    p = getProfile(user)
    role = p.role
    if role == 1:
        return False
    else:
        return True

def getCoreRole(user):
    checkCoreAccess(user)
    p = getProfile(user)
    return p.role

def changeRole(user, roleint):
    p = getProfile(user)
    p.role = roleint
    p.save()
    

def checkCoreToolAccess(user, toolid):
    getCoreRole(user)
    t = get_object_or_404(CoreTool, id=toolid)
    role = getCoreRole(user)

    if t.admin == True and role == 6:
        return True
    elif t.mod == True and role == 5:
        return True
    elif t.org == True and role == 4:
        return True
    elif t.staff == True and role == 3:
        return True
    elif t.rp == True and role == 2:
        return True
    else:
        return False
