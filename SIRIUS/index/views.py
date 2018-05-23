from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .forms import UserRegistrationForm, EvaluationGeneralForm
from django.contrib import messages
import datetime
from .decorators import student_required
from .models import Website, Review
# Create your views here.

def index(request):
	return render(request, "index/index.html", {})

def home(request):
    return render(request, "index/home.html", {})

def indicator(request):
    return render(request, "settings/indicator.html", {})

def features(request):
    return render(request, "settings/features.html", {})

def subfeatures(request):
    return render(request, "settings/subfeatures.html", {})

def attributes(request):
    return render(request, "settings/attributes.html", {})

@student_required
def evaluate(request):
	user = request.user
	form = EvaluationGeneralForm({'evaluator' : user.full_name})
	
	context = {'form' : form,
			   'today' : datetime.date.today()
			  }
				
	if request.method == 'POST':
		form = EvaluationGeneralForm(request.POST)
		if form.is_valid():
			# Obtengo datos del formulario
			evaluator = form.cleaned_data['evaluator']
			date = form.cleaned_data['date']
			website_name = form.cleaned_data['website_name']
			website_url = form.cleaned_data['website_url']
			website_description = form.cleaned_data['website_description']
			browser_name = form.cleaned_data['browser_name']
			browser_version = form.cleaned_data['browser_version']
			
			# Busco el website en la DB y lo creo si no existe
			try:
				website = Website.objects.get(name = website_name)
			except Website.DoesNotExist:
				try:
					website = Website.objects.get(url = website_url)
				except Website.DoesNotExist:
					website = Website.objects.create(
						url = website_url,
						name = website_name,
						description = website_description
						)
			
			# Creo objeto review	
			Review.objects.create(
				website = website,
				username = user,
				browser = browser_name,
				browser_version = browser_version,
				comment = ''
			)
			return HttpResponseRedirect(reverse('evaluate1', args=(), kwargs={}))
	
	return render(request, "evaluate/evaluate.html", {'form' : form})

def evaluate1(request):
    return render(request, "evaluate/1.html", {})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        User = get_user_model()
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['user']
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
                messages.error(request,'El usuario o correo ya existe, intenta con otro.')
                HttpResponseRedirect('/login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form' : form})
