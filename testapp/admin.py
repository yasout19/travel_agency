from django.contrib import admin
from .models import voyage,categorieVoyage,Reservation,Temoignage,Vols,Hotel
admin.site.register(voyage)
admin.site.register(categorieVoyage)
admin.site.register(Reservation)
admin.site.register(Temoignage)
admin.site.register(Hotel)
admin.site.register(Vols)

# Register your models here.
