from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm
# Create your views here.

def index(request):
	return render(request, "index/index.html", {})

def home(request):
    return render(request, "index/home.html", {})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        User = get_user_model()
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            full_name = userObj['full_name']
            telephone = userObj['telephone']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(user=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, full_name, telephone, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                raise forms.ValidationError('Parece que el username o correo ya existe. Prueba con otro.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form' : form})