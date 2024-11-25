from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from testapp.models import voyage, categorieVoyage, Temoignage
from account.models import profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .forms import createuserform
from django.contrib import messages
# Create your views here.
def index(request):
    voyages = voyage.objects.all()
    categories = categorieVoyage.objects.all()
    temoignages = Temoignage.objects.all()
    return render(request, 'index.html', {'voyages': voyages, 'categories': categories, 'temoignages': temoignages})
def about(request):
    return render(request,'about.html')
def service_app(request):
    temoignages = Temoignage.objects.all()
    return render(request, 'service.html', {'temoignages': temoignages})
def error_404(request, exception):
    return render(request, '404.html')
def contact(request):
    return render(request, 'contact.html')
def packages(request):
    voyages = voyage.objects.all()
    return render(request,'package.html',{'voyages':voyages})
def signup(request):
 if request.user.is_authenticated:
  return redirect('user:home')   # If user is already logged in then redirect him to homepage.
 else:
    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            profile.objects.create(
               user=user,
               username=username,
               email=form.cleaned_data.get('email'),
               phone="",
               adress="",
            )
            messages.success(request, "Account created for "+username)
            return redirect('testapp:signin')  # Redirect to the login page after successful registration
    else:
        form = createuserform()
    return render(request, 'registration/signup.html', {'form': form})
def signin(request):
 if request.user.is_authenticated:
    return redirect('user:home')   # If user is already logged in then redirect him to homepage.
 else:
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('user:home')
        else:
            messages.error(request, "Invalid Email or Password")
    
    return render(request, 'registration/signin.html')
def logout_view(request):
    logout(request)
    return redirect('testapp:signin')

def detail_voy(request, voyage_id):
    voyagey = get_object_or_404(voyage, pk=voyage_id)
    return render(request, 'details_voy.html', {'voyagey': voyagey})
def detail_categ(request, id_categorie):
    category = get_object_or_404(categorieVoyage, pk=id_categorie)
    voyages = voyage.objects.filter(categorie=category)
    return render(request, 'detail_categ.html', {'category': category, 'voyages':voyages})
def categ_view(request):
    categories = categorieVoyage.objects.all()
    context = {'categories': categories}
    return render(request, 'index.html', context)

def recherche_voy(request):
    voyages = voyage.objects.all()

    mot_cle = request.GET.get('mot', '')
    prix_min = request.GET.get('prix_min', None)
    prix_max = request.GET.get('prix_max', None)
    duree = request.GET.get('duree', None)
    categorie = request.GET.get('categorie', '')

    if mot_cle:
        voyages = voyages.filter(description__icontains=mot_cle)
    if prix_min is not None and prix_min != '':
        voyages = voyages.filter(prix__gte=prix_min)
    if prix_max is not None and prix_max != '':
        voyages = voyages.filter(prix__lte=prix_max)
    if duree is not None and duree != '':
        voyages = voyages.filter(duration=duree)
    if categorie:
        voyages = voyages.filter(categorie_titre_categ_icontains=categorie)

    return render(request, 'chercher_voy.html', {'voyages': voyages})