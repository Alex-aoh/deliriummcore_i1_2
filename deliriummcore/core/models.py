from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
 

class CoreTool(models.Model):

    name = models.CharField(max_length=30)

    verbosename = models.CharField(max_length=30)

    description = models.CharField(max_length=100)

    admin = models.BooleanField(default=False)
    mod = models.BooleanField(default=False)
    org = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    rp = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    


class CoreOrg(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "Org: " + self.name


class CoreBrand(models.Model):
    org = models.ForeignKey(CoreOrg, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    username = models.CharField(max_length=30)

    logo = models.FileField(upload_to='uploads/brands/logos', blank=True)

    def __str__(self) -> str:
        return "Brand: " + self.name







#User class
# class UserCore(models.Model):

#     user = models.OneToOneField(User, on_delete=models.CASCADE)



#     def __str__(self) -> str:
#         return str(self.user)

#     class Meta:

#         permissions = (
#             ("can_view_admin", "To see admin pages"),
#             ("can_view_mod", "To see mod pages"),
#             ("can_view_", "To see admin pages"),
#             ("can_view_staff", "To see staff pages"),
#             ("can_view_rp", "To see rp PAGES"),
#         )

#  #Add other custom permissions according to need.



    