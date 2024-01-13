from django.shortcuts import render,redirect
from django.http import HttpResponse
from testapp.models import voyage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
@login_required(login_url='testapp:signin')
def user_home(request):
    voyages=voyage.objects.all()
    return render(request,'user_home.html',{'voyages':voyages})

# Create your views here.
