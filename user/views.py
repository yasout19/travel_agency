from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from testapp.models import voyage, categorieVoyage, Reservation, Temoignage
from account.models import profile 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from testapp.forms import VoyageForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.core.mail import send_mail
from django.conf import settings
@login_required(login_url='testapp:signin')
def user_home(request):
    voyages=voyage.objects.all()
    categories = categorieVoyage.objects.all()
    temoignages = Temoignage.objects.all()
    return render(request,'user_home.html', {'voyages':voyages, 'categories':categories ,'temoignages': temoignages})
def contact(request):
    return render(request, 'user_contact.html')
def about(request):
    return render(request, 'about_user.html')
def services(request):
    temoignages = Temoignage.objects.all()
    return render(request, 'service_user.html', {'temoignages': temoignages})
def distination(request):
    return render(request, 'distination.html')
def error_404(request, exception):
    return render(request, '404.html')
def packages(request):
    voyages = voyage.objects.all()
    return render(request, 'offres.html', {'voyages' : voyages})
def detail_voyage(request, voyage_id):
    voyagey = get_object_or_404(voyage, pk=voyage_id)
    return render(request, 'detail_voyage.html', {'voyagey': voyagey})
def detail_categorie(request, id_categorie):
    category = get_object_or_404(categorieVoyage, pk=id_categorie)
    voyages = voyage.objects.filter(categorie=category)
    return render(request, 'detail_categorie.html', {'category': category, 'voyages':voyages})
def categorie_view(request):
    categories = categorieVoyage.objects.all()
    context = {'categories': categories}
    return render(request, 'user_home.html', context)
def packages(request):
    voyages = voyage.objects.all()
    return render(request,'offres.html',{'voyages':voyages})
def recherche_voyages(request):
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
        voyages = voyages.filter(categorie__titre_categ__icontains=categorie)

    return render(request, 'recherche_voyages.html', {'voyages': voyages})
def my_view(request):
    if request.method == 'POST':
        form = VoyageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index.html')
    else:
        form = VoyageForm()
    voyages = voyage.objects.all()
    return render(request, 'index.html', {'form': form, 'voyages': voyages})
def reservation(request, voyage_id):
    voyagee = get_object_or_404(voyage, pk=voyage_id)
    context = {
        'voyagee': voyagee,
    }
    return render(request, 'reservation.html', context)

def payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        datetime = request.POST.get('date_aller')
        destination = request.POST.get('destination')
        special_request = request.POST.get('message')
        number_of_persons = int(request.POST.get('number_of_persons'))
        baggage_weight_kg = int(request.POST.get('baggage_weight_kg'))
        prix = int(request.POST.get('prix_voyage'))

        base_price = prix
        excess_baggage_charge_per_kg = 50  # Frais par kilo
        excess_baggage_weight_kg = max(0, baggage_weight_kg - 5)  # Poids excédentaire de bagages
        excess_baggage_charge = excess_baggage_charge_per_kg * excess_baggage_weight_kg
        total_price = (base_price * number_of_persons) + excess_baggage_charge


        reservation = Reservation(
            name=name,
            email=email,
            datetime=datetime,
            destination=destination,
            special_request=special_request,
            number_of_persons=number_of_persons,
            baggage_weight_kg=baggage_weight_kg,
            total_price=total_price,
        )

        #reservation.save()
        return render(request, 'payment.html', {'reservation': reservation})

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas

def generate_pdf(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.method == 'POST':
        name = reservation.name
        email = reservation.email
        datetime = reservation.datetime
        destination = reservation.destination
        special_request = reservation.special_request
        number_of_persons = reservation.number_of_persons
        baggage_weight_kg = reservation.baggage_weight_kg
        prix = reservation.total_price

        # Créer un objet PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reservation.pdf"'

        # Créer un document PDF
        p = canvas.Canvas(response)
        p.setTitle("Détails de la réservation")

        # Ajouter le titre et le message de bienvenue
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Réservation :")
        p.drawString(100, 730, "Bienvenue chez {- YLAgency -}")

        # Ajouter l'en-tête de réservation
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 700, "Détails de la réservation :")

        # Ajouter les données de réservation au document
        p.setFont("Helvetica", 12)
        y_coordinate = 670
        p.drawString(100, y_coordinate, f"Nom : {name}")
        y_coordinate -= 20
        p.drawString(100, y_coordinate, f"Email : {email}")
        y_coordinate -= 20
        p.drawString(100, y_coordinate, f"Date de départ : {datetime}")
        y_coordinate -= 20
        p.drawString(100, y_coordinate, f"Destination : {destination}")
        y_coordinate -= 20
        p.drawString(100, y_coordinate, f"Nombre de Personnes : {number_of_persons} Personnes")
        y_coordinate -= 20
        p.drawString(100, y_coordinate, f"Poids de Bagage (kg) : {baggage_weight_kg} Kg")
        y_coordinate -= 20
        p.drawString(100, y_coordinate, f"Special Request : {special_request}")
        y_coordinate -= 20
        p.drawString(100, y_coordinate, f"Prix total : {prix} MAD")

        # Sauvegarder le document PDF
        p.showPage()
        p.save()

        return response

    else:
        # Gérer le cas où la méthode de la requête n'est pas POST
        # Peut-être rediriger l'utilisateur ou afficher un message d'erreur
        pass

def ajouter_avis(request):
    if request.method == 'POST':
        # Traitement du formulaire d'ajout d'avis
        nom = request.POST.get('nom', '')
        location = request.POST.get('location', '')
        message = request.POST.get('message', '')

        nouvel_avis = Temoignage.objects.create(nom=nom, location=location, message=message)

        # Afficher le formulaire pour ajouter un avis
        return render(request, 'user_contact.html')
    else:
        return render(request, 'user_contact.html')
def verification(request,price):
    Profile=profile.objects.get(user=request.user)
    if request.method == 'POST':
        if Profile.solde>price:
                name = request.POST.get('name')
                email = request.POST.get('email')
                datetime = request.POST.get('datetime')
                destination = request.POST.get('destination')
                special_request = request.POST.get('special_request')
                number_of_persons = int(request.POST.get('number_of_persons'))
                baggage_weight_kg = int(request.POST.get('baggage_weight_kg'))
                prix = int(request.POST.get('total_price'))

                base_price = prix
                excess_baggage_charge_per_kg = 50  # Frais par kilo
                excess_baggage_weight_kg = max(0, baggage_weight_kg - 5)  # Poids excédentaire de bagages
                excess_baggage_charge = excess_baggage_charge_per_kg * excess_baggage_weight_kg
                total_price = (base_price * number_of_persons) + excess_baggage_charge


                reservation = Reservation(
                    user=request.user,
                    name=name,
                    email=email,
                    datetime=datetime,
                    destination=destination,
                    special_request=special_request,
                    number_of_persons=number_of_persons,
                    baggage_weight_kg=baggage_weight_kg,
                    total_price=total_price,
                )
                Profile.solde-=price
                Profile.save()
                reservation.save()
                subject = 'Reservation Confirmation'
                message = f'Dear {Profile.user.username},\n\nYour reservation has been successfully confirmed.\n\nThank you for choosing our service.\n\nSincerely,\nThe Reservation Team'
                sender_email = settings.EMAIL_HOST_USER
                recipient_email = Profile.email
                send_mail(subject, message, sender_email, [recipient_email])
                return render(request,'paiement_reussi.html',{'reservation':reservation})
        else:
            return render(request,'paiement_echec.html')
        

