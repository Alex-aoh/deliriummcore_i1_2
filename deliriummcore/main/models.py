from email.policy import default
from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    USER = 1
    PR = 2
    STAFF = 3
    ORG = 4
    MOD = 5
    ADMIN = 6
      
    ROLE_CHOICES = (
    (USER, 'Usuario'),
    (PR, 'RP'),
    (STAFF, 'Staff'),
    (ORG, 'Organizador'),
    (MOD, 'Moderador'),
    (ADMIN, 'Administrador'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=1)

    def __str__(self) -> str:
        return str(self.user)


# You can create Role model separately and add ManyToMany if user has more than one role
      

