from django.contrib.auth.models import User
from oldcore.models import Seller

def checkSeller(user):
    if not Seller.objects.filter(user=user):
        Seller(user=user).save()