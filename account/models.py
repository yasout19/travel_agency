from django.contrib.auth.models import User
from django.db import models

class profile(models.Model):
 user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
 username=models.CharField(max_length=50,blank=True)
 email=models.CharField(max_length=50,blank=True)
 phone=models.CharField(max_length=50,blank=True)
 adress=models.CharField(max_length=50,blank=True)
 solde=models.PositiveIntegerField(default=0)
 def __str__(self):
  return str(self.user)

# Create your models here.
