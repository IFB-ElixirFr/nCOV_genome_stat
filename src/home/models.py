from django.contrib.auth.models import User
from django.db import models


class countries(models.Model):
   ADMIN = models.CharField(max_length=100,help_text="ISO_A3 code" )
   ISO_A3 = models.CharField(max_length=3,help_text="ISO_A3 code" )
   ISO_A2 = models.CharField(max_length=2, help_text="ISO_A2 code")
   geometry = models.JSONField()

   def __str__(self):
      return self.ADMIN


class applicationUser(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   IFB_member = models.BooleanField(help_text="Are you member of IFB ?", default=False)
   country = models.ForeignKey('countries', on_delete=models.CASCADE)
   location = models.CharField(max_length=500, help_text="Your laboratory",)
   position = models.CharField(max_length=500, help_text="Your position",)