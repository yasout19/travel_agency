from django.shortcuts import render,redirect
from django.http import HttpResponse
from testapp.models import voyage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from testapp.forms import createuserform
@login_required(login_url='testapp:signin')
def  index(request):
    return render(request,'nice-html/pages/index.html')
def  profil(request):
    if request.method == 'POST':
        form = createuserform(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,"Account updated for "+username)
            return redirect('dash:profil') 
    else:
        form = createuserform()
    return render(request,'nice-html/pages/pages-profile.html',{'form':form})
# Create your views here.
