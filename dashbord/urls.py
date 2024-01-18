from django.urls import path
from . import views
app_name = 'dash'
urlpatterns=[
    path('index/',views.index,name='home'),
    path('profil/',views.profil,name='profil'),

]