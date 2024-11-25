from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.http import HttpResponse
from testapp.models import voyage,Reservation
from account.models import profile
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from testapp.forms import createuserform,updateprofileform,PasswordChangingForm
from django.views import generic
from django.urls import reverse_lazy
@login_required(login_url='testapp:signin')
def  index(request):
    res=Reservation.objects.filter(user=request.user)
    return render(request,'nice-html/pages/mes_reservation.html',{'reservation':res})
class UserEditView(generic.UpdateView):
    form_class=updateprofileform
    template_name = 'nice-html/pages/pages-profile.html'
    success_url = reverse_lazy('dash:profil')

    def get_object(self, queryset=None):
        return profile.objects.get(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance = self.get_object()
        return form
class PasswordsChangeView(PasswordChangeView):
    form_class=PasswordChangingForm
    
def password_succes(request):
    return render(request,'nice-html/pages/password_succes.html')
def solde(request):
    Profile=profile.objects.get(user=request.user)
    Solde=Profile.solde
    return render(request,'nice-html/pages/mon_solde.html',{'solde':Solde})
def add_solde(request):
    Profile=profile.objects.get(user=request.user)
    if request.method=='POST':
        solde=float(request.POST.get("solde_amount", 0))
        Profile.solde+=solde
        Profile.save()
        return redirect("dash:solde")

    return render(request,'nice-html/pages/add_solde.html',{'solde':Profile.solde})
def minus_solde(request):
    Profile=profile.objects.get(user=request.user)
    if request.method=='POST':
        solde=float(request.POST.get("solde_amount", 0))
        Profile.solde-=solde
        Profile.save()
        return redirect("dash:solde")

    return render(request,'nice-html/pages/add_solde.html',{'solde':Profile.solde})
