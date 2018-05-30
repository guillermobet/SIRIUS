from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .forms import UserRegistrationForm, EvaluationGeneralForm, ReviewItemsForm, AddMetaHeuristicForm, AddMetaCriterionForm
from django.contrib import messages
import datetime
from .decorators import student_required
from .models import Website, Review, Criteria, MetaCriteria, MetaHeuristic
from django.db import IntegrityError
# Create your views here.

def index(request):
	return render(request, "index/index.html", {})

def home(request):
    return render(request, "index/home.html", {})
"""
def indicator(request):
    return render(request, "settings/indicator.html", {})

def features(request):
    return render(request, "settings/features.html", {})

def subfeatures(request):
    return render(request, "settings/subfeatures.html", {})

def attributes(request):
    return render(request, "settings/attributes.html", {})
"""
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
			review = Review.objects.create(
				website = website,
				username = user,
				browser = browser_name,
				browser_version = browser_version,
				date = date,
				comment = ''
			)
			kwargs = {'review_id' : review.pk}
			return HttpResponseRedirect(reverse('evaluate_items', args=(), kwargs=kwargs))
	
	return render(request, "evaluate/evaluate.html", {'form' : form})

@student_required
def evaluate_items(request, review_id):
	
	user = request.user
	form = ReviewItemsForm()
	heuristics = MetaHeuristic.objects.all()
	context = {'form' : form,
			   'heuristics' : heuristics
			  }
	
	if request.method == 'POST':
		form = ReviewItemsForm(request.POST)
		if form.is_valid():
			review = Review.objects.get(pk = review_id)
			for value in form.cleaned_data:
				split = value.split('_')
				criteria_id = int(split[3])
				meta_criteria = MetaCriteria.objects.get(pk = criteria_id)
				Criteria.objects.create(
					review = review,
					meta_criteria = meta_criteria,
					value = form.cleaned_data[value]
				)
			return HttpResponseRedirect(reverse('home', args=(), kwargs={}))
			print('Form is valid!')
	
	return render(request, "evaluate/evaluateItems.html", context)

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
            password2 =  userObj['password_confirmation']
            if not (User.objects.filter(user=username).exists() or User.objects.filter(email=email).exists()):
                if not (password and password2 and password != password2):
                    User.objects.create_user(username, email, full_name, telephone, password)
                    user = authenticate(username = username, password = password)
                    login(request, user)
                    return HttpResponseRedirect('/home')
                else:
                    messages.error(request,"Passwords don't match")
                    HttpResponseRedirect('/register')
            else:
                messages.error(request,'El usuario o correo ya existe, intenta con otro.')
                HttpResponseRedirect('/login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form' : form})

@student_required
def reviews(request):
	user = request.user
	
	reviews = Review.objects.filter(username = user)
	context = {'user' : user,
			   'reviews' : reviews
			   }
	
	return render(request, 'reviews/reviews.html', context)
	
@student_required
def reviews_edit(request, review_id):
	user = request.user
	review = Review.objects.get(id = review_id)
	criteria = Criteria.objects.filter(review = review)
	print(criteria)
	context = {'user' : user,
			   'review' : review,
			   'criteria' : criteria
			   }
	return render(request, 'reviews/ver_review.html', context)
	
def meta_heuristics(request):
	
	if request.method == 'POST':
		form = AddMetaHeuristicForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			acronym = form.cleaned_data['acronym']
			try:
				MetaHeuristic.objects.create(name = name, acronym = acronym)
			except IntegrityError:
				pass
				#display message
			
	heuristics = MetaHeuristic.objects.all()
	form = AddMetaHeuristicForm()
	context = {'heuristics' : heuristics,
			   'form' : form
			   }
	return render(request, 'settings/heuristics.html', context)
	
def delete_meta_heuristics(request, meta_heuristic_id):
	MetaHeuristic.objects.get(pk = meta_heuristic_id).delete()
	return HttpResponseRedirect(reverse('meta_heuristics', args=(), kwargs={}))
	
def meta_criteria(request):
	
	if request.method == 'POST':
		form = AddMetaCriterionForm(request.POST)
		if form.is_valid():
			heuristic = form.cleaned_data['heuristic']
			name = form.cleaned_data['name']
			acronym = form.cleaned_data['acronym']
			atribute = form.cleaned_data['atribute']
			metric = form.cleaned_data['metric']
			try:
				MetaCriteria.objects.create(
					heuristic = heuristic,
					name = name,
					acronym = acronym,
					atribute = atribute,
					metric = metric
					)
			except IntegrityError:
				print('No lo cree el mio')
				pass
				#display message
			
	criteria = MetaCriteria.objects.all()
	form = AddMetaCriterionForm()
	context = {'criteria' : criteria,
			   'form' : form
			   }
	return render(request, 'settings/criteria.html', context)

def delete_meta_criterion(request, meta_criterion_id):
	MetaCriteria.objects.get(pk = meta_criterion_id).delete()
	return HttpResponseRedirect(reverse('meta_criteria', args=(), kwargs={}))
