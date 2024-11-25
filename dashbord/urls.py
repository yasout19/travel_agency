from django.urls import path
from . import views
from django.urls import reverse_lazy
app_name = 'dash'
urlpatterns=[
    path('index/',views.index,name='home'),
    path('profil/',views.UserEditView.as_view(),name='profil'),
    path('password/',views.PasswordChangeView.as_view(template_name = 'nice-html/pages/password.html',success_url = reverse_lazy('dash:password_succes')),name='password'),
    path('password_succes',views.password_succes,name='password_succes'),
    path('mon_solde/',views.solde,name='solde'),
    path('add_solde/',views.add_solde,name='add_solde'),
    path('minus_solde/',views.minus_solde,name='minus_solde'),
]