from django.db import models
from django.contrib.auth.models import User
class categorieVoyage(models.Model):
    image = models.ImageField(upload_to='voyage_images/', null=True, blank=True)
    titre_categ = models.CharField(max_length=50, blank=True)
    description_categ = models.CharField(max_length=300, blank=True)
    description_courte = models.CharField(max_length=100, blank=True, null=True)
    reduction_percent = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.titre_categ
class Vols(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name 

class voyage(models.Model):
    image = models.ImageField(upload_to='voyage_images/', null=True, blank=True)
    ville_origine = models.CharField(max_length=50,blank=True)
    ville_destination = models.CharField(max_length=50,blank=True)
    date_aller = models.DateField(null=True,blank=True)
    date_retour = models.DateField(null=True,blank=True)
    description = models.CharField(max_length=300, blank=True)
    prix = models.IntegerField(default=0)
    nombre_personnes = models.IntegerField(default=1)
    categorie = models.ForeignKey(categorieVoyage, on_delete=models.CASCADE, default=1)
    duration = models.IntegerField(null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    vols = models.ForeignKey(Vols, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.ville_origine} - {self.ville_destination}"

    def save(self, *args, **kwargs):
        self.duration = self.calculate_duration()
        super().save(*args, **kwargs)
    def calculate_duration(self):
        if self.date_aller and self.date_retour:
            return (self.date_retour - self.date_aller).days
        else:
            return 0

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=100,blank=True)
    email = models.EmailField()
    datetime = models.DateTimeField(null=True,blank=True)
    destination = models.CharField(max_length=100,blank=True)
    special_request = models.TextField(blank=True)
    number_of_persons = models.PositiveIntegerField()
    baggage_weight_kg = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(default=0,blank=True,)

    def __str__(self):
        return f"{self.name}'s Reservation"


class Temoignage(models.Model):
    nom = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.nom
    
