from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from testapp.models import voyage,categorieVoyage,Reservation,Hotel,Vols
from account.models import profile
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from testapp.forms import createuserform,updateprofileform,PasswordChangingForm,CustomUserChangeForm
from django.views import generic,View
from django.urls import reverse_lazy
from datetime import datetime
from django.db.models import Sum
@login_required(login_url='testapp:signin')
def  index(request):
    first_five_reservations = Reservation.objects.all()[:5]
    total_users = User.objects.count()
    total_price = Reservation.objects.aggregate(total_price=Sum('total_price'))['total_price']
    if total_price is None:
     total_price = 0
    return render(request,'nice-html/pages/home.html',{'price':total_price,'total_users':total_users,'res':first_five_reservations})
class UserEditView(generic.UpdateView):
    form_class=CustomUserChangeForm
    template_name = 'nice-html/pages/profile.html'
    success_url = reverse_lazy('dash_admin:profil')
    def get_queryset(self):
        # Return the queryset for the currently logged-in user
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user
class PasswordsChangeView(PasswordChangeView):
    form_class=PasswordChangingForm
    
def password_succes(request):
    return render(request,'nice-html/pages/password2_succes.html')
def showusers(request):
    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            try:
                User.objects.get(username=username)
                messages.error(request, "Cet utilisateur existe déjà")
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email=email, password=password)
                # You can also create a profile here if needed
                messages.success(request, "Utilisateur créé avec succès.")
    users=User.objects.all()
    return render(request,'nice-html/pages/users.html',{'users':users})
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('dash_admin:users')
def categories(request):
    if request.method == 'POST':
        Image=request.FILES["image"]
        title=request.POST["title"]
        description=request.POST["description"]
        percentage=request.POST["percentage"]
        new_categ=categorieVoyage(image=Image,titre_categ =title,description_courte=description,reduction_percent=percentage)
        new_categ.save()
    cat=categorieVoyage.objects.all()
    return render(request,'nice-html/pages/categorie_infos.html',{'categories':cat})
def delete_cat(request, cat_id):
    cat = get_object_or_404(categorieVoyage, id=cat_id)
    cat.delete()
    return redirect('dash_admin:categories')
def voyages(request):
    if request.method == 'POST':
        Image=request.FILES["image"]
        ville_origine = request.POST["ville_origine"]
        ville_destination = request.POST["ville_destination"]
        date_aller_str = request.POST["date_aller"]
        date_retour_str = request.POST["date_retour"]
        description = request.POST["description"]
        prix = request.POST["prix"]
        nombre_personnes = request.POST["nombre_personnes"]
        categorie_titre_categ = request.POST["categorie"]
        vol_name= request.POST["vols"]
        hot_name= request.POST["hotels"]
        date_aller = datetime.strptime(date_aller_str, '%Y-%m-%d').date()
        date_retour = datetime.strptime(date_retour_str, '%Y-%m-%d').date()
        vol=Vols.objects.get(name=vol_name)
        hot=Hotel.objects.get(name=hot_name)
        cat=categorieVoyage.objects.get(titre_categ=categorie_titre_categ)
        new_voy = voyage(
            image=Image,
            ville_origine=ville_origine,
            ville_destination=ville_destination,
            date_aller=date_aller,
            date_retour=date_retour,
            description=description,
            prix=prix,
            nombre_personnes=nombre_personnes,
            categorie=cat,
            vols=vol,
            hotel=hot,
            
        )
        new_voy.save()
    vol=Vols.objects.all()
    hot=Hotel.objects.all()
    cat=categorieVoyage.objects.all()
    voy=voyage.objects.all()
    return render(request,'nice-html/pages/voyages.html',{'voyages':voy,'categories':cat,'vols':vol,'hotels':hot})
def reservation(request):
    res=Reservation.objects.all()
    return render(request,'nice-html/pages/reservation.html',{'reservation':res})
def delete_voyage(request, cat_id):
    cat = get_object_or_404(voyage, id=cat_id)
    cat.delete()
    return redirect('dash_admin:voyages')
def edit_cat(request, cat_id):
    cat = get_object_or_404(categorieVoyage, id=cat_id)
    if request.method == 'POST':
        Image=request.FILES["image"]
        title=request.POST["title"]
        description=request.POST["discription"]
        percentage=request.POST["pourcentage"]
        cat.image=Image
        cat.titre_categ=title
        cat.description_courte=description
        cat.reduction_percent=percentage
        cat.save()
        return redirect("dash_admin:categories")
    return render(request,'nice-html/pages/edit_categ.html',{'cat':cat})
def edit_voy(request, voy_id):
    voy= get_object_or_404(voyage, id=voy_id)
    cat=categorieVoyage.objects.all()
    vol=Vols.objects.all()
    hot=Hotel.objects.all()

    if request.method == 'POST':
        Image = request.FILES.get("image")  # Use get() to avoid KeyError if 'image' is missing
        ville_origine = request.POST.get("ville_origine", "")  # Use get() with a default value
        ville_destination = request.POST.get("ville_destination", "")  # Same here
        date_aller_str = request.POST.get("date_aller", "")  # Same here
        date_retour_str = request.POST.get("date_retour", "")  # Same here
        description = request.POST.get("description", "")  # Same here
        prix = int(request.POST.get("prix", 0))  # Convert to integer, use 0 as default if not provided
        nombre_personnes = int(request.POST.get("nombre_personnes", 1))  # Same here, default to 1
        categorie_titre_categ = request.POST.get("categorie", "")  # Same here
        hot_name = request.POST.get("hotel", "") 
        vol_name = request.POST.get("vol", "") 
        date_aller = datetime.strptime(date_aller_str, '%Y-%m-%d').date() if date_aller_str else None  # Handle empty string case
        date_retour = datetime.strptime(date_retour_str, '%Y-%m-%d').date() if date_retour_str else None  # Handle empty string case
        vol=Vols.objects.get(name=vol_name)
        hot=Hotel.objects.get(name=hot_name)
        # Create a new voyage object
        
        voy.image=Image
        voy.ville_origine=ville_origine
        voy.ville_destination=ville_destination
        voy.date_aller=date_aller
        voy.date_retour=date_retour
        voy.description=description
        voy.prix=prix
        voy.nombre_personnes=nombre_personnes
        categorie=categorieVoyage.objects.get(titre_categ=categorie_titre_categ)  # Retrieve the categorie object based on its title
        voy.categorie=categorie
        voy.hotel=hot
        voy.vols=vol
        
        # Save the voyage object
        voy.save()

        return redirect("dash_admin:voyages")
    return render(request,'nice-html/pages/edit_voy.html',{'voy':voy,'categories':cat,'hotels':hot,'vols':vol})
def hotels(request):
    if request.method == 'POST':
        name=request.POST["name"]
        location=request.POST["location"]
        rating=request.POST["rating"]
        new_hot=Hotel(name=name,location=location,rating=rating)
        new_hot.save()
    hot=Hotel.objects.all()
    return render(request,'nice-html/pages/hotels.html',{'hotels':hot})
def delete_hot(request, hot_id):
    hot= get_object_or_404(Hotel, id=hot_id)
    hot.delete()
    return redirect('dash_admin:hotels')
def vols(request):
    if request.method == 'POST':
        name=request.POST["name"]
        rating=request.POST["rating"]
        new_vol=Vols(name=name,rating=rating)
        new_vol.save()
    vol=Vols.objects.all()
    return render(request,'nice-html/pages/vols.html',{'vols':vol})
def delete_vol(request, vol_id):
    vol= get_object_or_404(Vols, id=vol_id)
    vol.delete()
    return redirect('dash_admin:vols')
def edit_vol(request, vol_id):
    vol = get_object_or_404(Vols, id=vol_id)
    if request.method == 'POST':
        
       name=request.POST["name"]
       try:
        rating_str = request.POST["rating"]
        rating = float(rating_str)
       except KeyError:
    # Handle the case where "rating" key is not present in the POST request
        rating = 0.0  # or any other default value you prefer
       except ValueError:
    # Handle the case where the value of "rating" is not a valid float
    # For example, you can set rating to None or any other default value
         rating = None
       vol.name=name
       vol.rating=float(rating)
       vol.save()
       return redirect("dash_admin:vols")
    return render(request,'nice-html/pages/edit_vol.html',{'vol':vol})
def edit_hot(request, hot_id):
    hot = get_object_or_404(Hotel, id=hot_id)
    if request.method == 'POST':
        
       name=request.POST["name"]
       location=request.POST["location"]
       try:
        rating_str = request.POST["rating"]
        rating = float(rating_str)
       except KeyError:
    # Handle the case where "rating" key is not present in the POST request
        rating = 0.0  # or any other default value you prefer
       except ValueError:
    # Handle the case where the value of "rating" is not a valid float
    # For example, you can set rating to None or any other default value
         rating = None
       hot.name=name
       hot.location=location
       hot.rating=float(rating)
       hot.save()
       return redirect("dash_admin:hotels")
    return render(request,'nice-html/pages/edit_hot.html',{'hot':hot})
    