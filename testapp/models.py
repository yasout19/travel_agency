from django.contrib.auth.models import AbstractUser
from django.db import models
class voyage(models.Model):
 country=models.CharField(max_length=50)
 discription=models.CharField(max_length=300,blank=True)
 date = models.DateField()
 price=models.IntegerField(default=0)
 def __str__(self):
  return self.country
# Create your models here.

