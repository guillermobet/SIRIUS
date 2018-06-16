from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from .forms import *
from django.contrib import messages
import datetime
from .decorators import student_required, admin_required
from .models import Website, Review, Criteria, MetaCriteria, MetaHeuristic
from django.db import IntegrityError
from django.template.loader import render_to_string
from .scoreEvaluator import get_up

def index(request):
	return render(request, "index/index.html", {})

def home(request):
	return render(request, "index/home.html", {})

def perfil(request):
	#user1=request.user
	error=False
	if request.method == 'POST':
		form = UserUpdateForm(request.POST)
		if form.is_valid():
			#user = User.objects.get(user=user1)
			user = request.user
			#user.telephone=request.POST.get('telephone')                    
			user.telephone = form.cleaned_data['telephone']
			#user.email=request.POST.get('email') 
			new_email = form.cleaned_data['email']
			#password=request.POST.get('password')
			password = form.cleaned_data['password']
			#password2=request.POST.get('password_confirmation')
			password2 = form.cleaned_data['password_confirmation']
			#if (User.objects.filter(email=user.email).exists() and user.email != user1.email):
			if (User.objects.exclude(pk = user.pk).filter(email = new_email).exists()):
				messages.error(request,"El email ya existe")
				error=True
			if (password and password2 and password != password2):
				messages.error(request,"Contraseña no coincide")
				error=True
			if(password != ''):
				#user.password = password
				# v--- Con esto se guarda la contrasena encriptada
				user.set_password(password)
					
			if not error:
				user.email = new_email
				user.save()
				messages.success(request, 'Usuario editado de manera exitosa')
				user = authenticate(username = user.user, password = user.password)
				login(request, user)

		return HttpResponseRedirect(reverse('perfil', args=(), kwargs={}))
	
	data = {'full_name' : request.user.full_name,
			'email' : request.user.email,
			'telephone' : request.user.telephone,
			'user' : request.user.user
			}
	form = UserUpdateForm(data)
	context = { 'form': form}
	return render(request, "index/perfil.html", context)


@student_required
def evaluate(request):
	user = request.user
	form = EvaluationGeneralForm(user, {'evaluator' : user.full_name})
	
	context = {'form' : form,
			   'today' : datetime.date.today()
			  }
				
	if request.method == 'POST':
		form = EvaluationGeneralForm(user, request.POST)
		if form.is_valid():
			# Getting form data
			evaluator = form.cleaned_data['evaluator']
			date = form.cleaned_data['date']
			website = form.cleaned_data['website']
			browser_name = form.cleaned_data['browser_name']
			browser_version = form.cleaned_data['browser_version']
						
			# Create Review object
			try:
				review = Review.objects.create(
					website = website,
					username = user,
					browser = browser_name,
					browser_version = browser_version,
					date = date,
					UP = 0.0,
					comment = ''
				)
			
			# In case the user has already reviewed this site, it will raise an error and redirect to the review
			except IntegrityError:
				messages.error(request, 'Usted ya hizo un review de este website')
				review = Review.objects.get(website = website, username = user)
				kwargs = {'review_id' : review.pk}
				return HttpResponseRedirect(reverse('see_review', args=(), kwargs=kwargs))


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
			criteria_list = []
			for value in form.cleaned_data:
				split = value.split('_')
				if(len(split) != 4):
					continue
				criteria_id = int(split[3])
				meta_criteria = MetaCriteria.objects.get(pk = criteria_id)
				crit = Criteria.objects.create(
					review = review,
					meta_criteria = meta_criteria,
					value = form.cleaned_data[value]
				)
				criteria_list.append(crit)
			
			review.UP = get_up(criteria_list, review.website.type)
			review.save()
				
			messages.success(request, 'Review registrado con exito, Porcentaje de Usabilidad obtenido: %.2f%%'%review.UP)
			return HttpResponseRedirect(reverse('home', args=(), kwargs={}))
	
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
					messages.error(request,"Las contraseñas no coinciden")
					HttpResponseRedirect('/register')
			else:
				messages.error(request,'El usuario o correo ya existe, intenta con otro.')
				HttpResponseRedirect('/register')
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
def see_review(request, review_id):
	user = request.user
	try:
		review = Review.objects.get(id = review_id)
	except Review.DoesNotExist:
		messages.error(request, 'La review que tratas de acceder no existe')
		return HttpResponseRedirect(reverse('reviews', args=(), kwargs={}))
	
		
	review_items = {}
	
	# Armo diccionario con el meta modelo y sus valores asignados
	heuristics = MetaHeuristic.objects.all()
	for heuristic in heuristics:
		review_items[(heuristic.name, str(heuristic.pk))] = []
		#review_items[heuristic.name] = []
		meta_criteria = MetaCriteria.objects.filter(heuristic = heuristic)
		
		# Para cada meta criterio busco su valor en el review, si no existe pongo un guion
		for meta_criterion in meta_criteria:
			try:
				criterion_value = Criteria.objects.get(review = review, meta_criteria = meta_criterion).value
			except Criteria.DoesNotExist:
				criterion_value = '-'
			"""
			review_items[heuristic.name].append({'meta_criterion' : meta_criterion,
												 'criterion_value' : criterion_value
												 })
			"""
			review_items[(heuristic.name, str(heuristic.pk))].append({'meta_criterion' : meta_criterion,
												 'criterion_value' : criterion_value
												 })
		
	context = {'user' : user,
			   'review' : review,
			   'review_items' : review_items
			   }
	return render(request, 'reviews/ver_review.html', context)
	
def edit_review(request, review_id):
	
	# Process inputed data and save results
	if request.method == 'POST':
		form = ReviewItemsForm(request.POST)
		if form.is_valid():
			review = Review.objects.get(pk = review_id)
			criteria_list = []
			for value in form.cleaned_data:
				split = value.split('_')
				if(len(split) != 4):
					continue
				criteria_id = int(split[3])
				meta_criteria = MetaCriteria.objects.get(pk = criteria_id)
				
				# Look for the criterion and create it if does not exist
				try:
					criterion = Criteria.objects.get(review = review, meta_criteria = meta_criteria)
					criterion.value = form.cleaned_data[value]
					criterion.save()
				except Criteria.DoesNotExist:
					criterion = Criteria.objects.create(review = review,
											meta_criteria = meta_criteria,
											value = form.cleaned_data[value])
				criteria_list.append(criterion)
				
			review.UP = get_up(criteria_list, review.website.type)
			review.save()
			messages.success(request, 'Review editada de manera exitosa, Porcentaje de Usabilidad obtenido: %.2f%%'%review.UP)
			return HttpResponseRedirect(reverse('reviews', args=(), kwargs={}))
	
	# Search for the requested review and redirect if it doesnt exist
	try:
		review = Review.objects.get(pk = review_id)
	except Review.DoesNotExist:
		messages.error(request, 'La Review que tratas de editar no existe')
		return HttpResponseRedirect(reverse('reviews', args=(), kwargs={}))
	
	# Setting up data dict with the data from the review for the form
	data = {}
	heuristics = MetaHeuristic.objects.all()
	for heuristic in heuristics:
		data['H_'+str(heuristic.pk)] = None
		meta_criteria = MetaCriteria.objects.filter(heuristic = heuristic)
		for meta_criterion in meta_criteria:
			try:
				criterion = Criteria.objects.get(meta_criteria = meta_criterion, review = review)
				criterion_value = criterion.value
			except Criteria.DoesNotExist:
				criterion_value = None
			data['H_'+str(heuristic.pk)+'_C_'+str(meta_criterion.pk)] = criterion_value
		data['H_'+str(heuristic.pk)+'_END'] = None
		
	form = ReviewItemsForm(data)
	context = {'form' : form,
			   'review' : review
			   }
	
	return render(request, 'reviews/edit_review.html', context)

@admin_required
def meta_heuristics(request, meta_heuristic_id = None):
	
	if request.method == 'POST':
		form = MetaHeuristicForm(request.POST)
		if form.is_valid():
			
			# Creating new MetaHeuristic
			if(meta_heuristic_id == None):
				name = form.cleaned_data['name']
				acronym = form.cleaned_data['acronym']
				try:
					MetaHeuristic.objects.create(name = name, acronym = acronym)
					messages.success(request, 'Heuristica creada exitosamente')
				except IntegrityError:
					messages.error(request, 'Una Heuristica con estas caracteristicas ya esta registrada en el sistema')
			
			# Editing existing MetaHeuristic
			else:
				heuristic = MetaHeuristic.objects.get(pk = meta_heuristic_id)
				heuristic.name = form.cleaned_data['name']
				heuristic.acronym = form.cleaned_data['acronym']
				try:
					heuristic.save()
					messages.success(request, 'Heuristica editada exitosamente')
				except IntegrityError:
					messages.error(request, 'Una Heuristica con estas caracteristicas ya esta registrada en el sistema')
	
	# Heuristics for showing
	heuristics = MetaHeuristic.objects.all()
	
	# Edit MetaHeuristic form
	if(meta_heuristic_id != None):
		try:
			heuristic = MetaHeuristic.objects.get(pk = meta_heuristic_id)
		except MetaHeuristic.DoesNotExist:
			messages.error(request, 'La Heuristica que esta tratando de editar no existe')
			return HttpResponseRedirect(reverse('meta_heuristics', args=(), kwargs={}))
			
		data = {'name' : heuristic.name,
				'acronym' : heuristic.acronym
				}
		form = MetaHeuristicForm(data)
		
	# Create MetaHeuristic form
	else:
		form = MetaHeuristicForm()
	
	context = {'heuristics' : heuristics,
			   'form' : form
			   }
				   
	return render(request, 'settings/heuristics.html', context)

@admin_required	
def delete_meta_heuristics(request, meta_heuristic_id):
	try:
		MetaHeuristic.objects.get(pk = meta_heuristic_id).delete()
		messages.success(request, 'Heuristica eliminada exitosamente')
	except MetaHeuristic.DoesNotExist:
		messages.error(request, 'La Heuristica que esta tratando de eliminar no existe')
	
	return HttpResponseRedirect(reverse('meta_heuristics', args=(), kwargs={}))

@admin_required
def meta_criteria(request, meta_criterion_id=None):
	filterCriteria = False
	
	if request.method == 'POST':
		if('criterion_form' in request.POST):
			form = MetaCriterionForm(request.POST)
			if form.is_valid():
				
			# Creating new MetaCriteria
				if(meta_criterion_id == None):
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
						messages.success(request, 'Sub-Heuristica creada exitosamente!')
					except IntegrityError:
						messages.error(request, 'Una Sub-Heuristica con estas caracteristicas ya esta registrada en el sistema')
						
				# Editing existing MetaCriteria
				else:
					criterion = MetaCriteria.objects.get(pk = meta_criterion_id)
					criterion.heuristic = form.cleaned_data['heuristic']
					criterion.name = form.cleaned_data['name']
					criterion.acronym = form.cleaned_data['acronym']
					criterion.metric = form.cleaned_data['metric']
					criterion.atribute = form.cleaned_data['atribute']
					try:
						criterion.save()
						messages.success(request, 'Sub-Heuristica editada exitosamente')
					except IntegrityError:
						messages.error(request, 'Una Sub-Heuristica con estas caracteristicas ya esta registrada en el sistema')
					
		
		# Getting data from filtering form		
		filterForm = FilterMetaCriteriaForm(request.POST)
		if filterForm.is_valid():
			filterHeuristic = filterForm.cleaned_data['heuristic']
			if(filterHeuristic != None):
				filterCriteria = True
	
	form = MetaCriterionForm()
	filterForm = FilterMetaCriteriaForm()
	
	# Filtering criteria for showing
	if(filterCriteria):
		criteria = 	MetaCriteria.objects.filter(heuristic = filterHeuristic)
		filterForm = FilterMetaCriteriaForm(initial={'heuristic' : filterHeuristic})
	else:
		criteria = MetaCriteria.objects.all()
		
	
	# Edit MetaCriteria form
	if(meta_criterion_id != None):
		try:
			criterion = MetaCriteria.objects.get(pk = meta_criterion_id)
		except MetaCriteria.DoesNotExist:
			messages.error(request, 'El Criterio que esta tratando de editar no existe')
			return HttpResponseRedirect(reverse('meta_criteria', args=(), kwargs={}))
			
		data = {'heuristic' : criterion.heuristic,
				'name' : criterion.name,
				'acronym' : criterion.acronym,
				'metric' : criterion.metric,
				'atribute' : criterion.atribute
				}
		form = MetaCriterionForm(data)
		
	# Create MetaCriteria form	
	else:
		form = MetaCriterionForm()
		
	context = {'criteria' : criteria,
			   'form' : form,
			   'filter_form' : filterForm
			   }
			   
	return render(request, 'settings/criteria.html', context)

@admin_required
def delete_meta_criterion(request, meta_criterion_id):
	try:
		MetaCriteria.objects.get(pk = meta_criterion_id).delete()
		messages.success(request, 'Criterio eliminado exitosamente')
	except MetaCriteria.DoesNotExist:
		messages.error(request, 'El Criterio que esta tratando de eliminar no existe')
		
	return HttpResponseRedirect(reverse('meta_criteria', args=(), kwargs={}))


def websites(request, website_id = None):
	
	if request.method == 'POST':
		form = WebsiteForm(request.POST)
		if form.is_valid():
			
			# Creating new Website
			if(website_id == None):
				name = form.cleaned_data['website_name']
				url = form.cleaned_data['website_url']
				type = form.clenaed_data['website_type']
				description = form.cleaned_data['website_description']
				try:
					Website.objects.create(
						name = name,
						url = url,
						type = type,
						description = description
					)
					messages.success(request, 'Website creado exitosamente')
				except IntegrityError:
					messages.error(request, 'Un Website con estas caracteristicas ya esta registrado en el sistema')
			
			# Editing existing Website
			else:
				website = Website.objects.get(pk = website_id)
				website.name = form.cleaned_data['website_name']
				website.url = form.cleaned_data['website_url']
				website.type = form.cleaned_data['website_type']
				website.description = form.cleaned_data['website_description']
				try:
					website.save()
					messages.success(request, 'Website editado exitosamente')
				except IntegrityError:
					messages.error(request, 'Un Website con estas caracteristicas ya esta registrado en el sistema')
	
	# Websites for showing
	websites = Website.objects.all()
	
	# Edit Website form
	if(website_id != None):
		try:
			website = Website.objects.get(pk = website_id)
		except Website.DoesNotExist:
			messages.error(request, 'El Website que esta tratando de editar no existe')
			return HttpResponseRedirect(reverse('websites', args=(), kwargs={}))
			
		data = {'website_name' : website.name,
				'website_url' : website.url,
				'website_type' : website.type,
				'website_description' : website.description
				}
		form = WebsiteForm(data)
	# Create Website form
	else:
		form = WebsiteForm()
	
	
	context = {'form' : form,
			   'websites' : websites}
	return render(request, 'websites/websites.html', context)
