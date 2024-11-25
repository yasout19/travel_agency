from django.urls import path
from . import views
app_name = 'user'
urlpatterns=[
    path('index/', views.user_home, name='home'),
    path('contact/', views.ajouter_avis, name='contact'),
    path('detail_categorie/<int:id_categorie>/', views.detail_categorie, name='detail_categorie'),
    path('packages/',views.packages, name='package'),
    path('recherche_voyages/', views.recherche_voyages, name='recherche_voyages'),
    path('reservation/<int:voyage_id>/', views.reservation, name='reservation'),
    path('payment/', views.payment, name='payment'),
    path('about/', views.about, name='about'),
    path('service/', views.services, name='service'),
    path('distination/', views.distination,name='distination'),
    path('packages/', views.packages,name='package'),
    path('voyage/<int:voyage_id>/', views.detail_voyage, name='detail-voyage'),
    path('generate_pdf/<int:reservation_id>/', views.generate_pdf, name='generate_pdf'),
    path('verification/<int:price>/', views.verification, name='verification'),

]