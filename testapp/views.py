from django.shortcuts import render,redirect
from django.http import HttpResponse
from testapp.models import voyage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .forms import createuserform
from django.contrib import messages
# Create your views here.
def index(request):
    voyages=voyage.objects.all()
    return render(request,'index.html',{'voyages':voyages})
def about(request):
    return render(request,'about.html')
def services(request):
    return render(request,'service.html')
def distination(request):
    return render(request,'distination.html')
def error_404(request, exception):
    return render(request, '404.html')
def contact(request):
    return render(request,'contact.html')
def packages(request):
    voyages=voyage.objects.all()
    return render(request,'package.html',{'voyages':voyages})
def signup(request):
 if request.user.is_authenticated:
  return redirect('user:home')   # If user is already logged in then redirect him to homepage.
 else:
    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,"Account created for "+username)
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
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('user:home')
        else:
            messages.error(request,"Invalid Email or Password")
    
    return render(request, 'registration/signin.html')
def logout_view(request):
    logout(request)
    return redirect('testapp:signin')