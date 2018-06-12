from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import User, MetaHeuristic, MetaCriteria
from django.utils.safestring import mark_safe
import datetime


class UserRegistrationForm(forms.Form):
    user = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
        widget = forms.TextInput({"placeholder": "Username *"})

    )
    full_name = forms.CharField(
        required = True,
        label = 'Nombre Completo',
        max_length = 60,
        widget = forms.TextInput({"placeholder": "Nombre Completo *"})

    )
    telephone= forms.CharField(
        required = False,
        label = 'Teléfono',
        max_length = 11,
        widget = forms.TextInput({"placeholder": "Teléfono"})

    )
    email = forms.EmailField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget = forms.TextInput({"placeholder": "Email *"})
    )
    password = forms.CharField(
        required = True,
        label = 'Contraseña',
        max_length = 32,
        widget = forms.PasswordInput({"placeholder": "Contraseña *"})
    )
    password_confirmation = forms.CharField(
        required = True,
        label = 'Confirmación contraseña',
        max_length = 32,
        widget = forms.PasswordInput({"placeholder": "Confirmación contraseña *"})
    )

    def clean_password_confirmation(self):
        # Check that the two password entries match
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_confirmation']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
    
    def clean_user(self):
        users = self.cleaned_data['user']
        if User.objects.filter(user = users).exists():
            raise forms.ValidationError("Username already exists.")
        return users
        
class EvaluationGeneralForm(forms.Form):
	evaluator = forms.CharField(
		required = True,
		label = 'Evaluador',
		max_length = 60,
		widget = forms.TextInput({"placeholder": "Ej. Maigualida Perez",
								   "readonly": True
								   })
	)
	date = forms.DateField(
		required = True,
		label = 'Fecha de la Evaluación',
		initial = datetime.date.today,
	)
	website_name = forms.CharField(
		required = True,
		label = "Nombre del Website",
		max_length = 100,
		widget = forms.TextInput({"placeholder": "Ej. Google"})
	)
	website_url = forms.URLField(
		required = True,
		label = "URL del Website",
		widget = forms.URLInput({'placeholder': 'Ej. https://www.google.com/'})
	)
	website_description = forms.CharField(
		required = True,
		label = "Descripción del Website",
		widget = forms.TextInput({"placeholder": 'Ej. Búsqueda'})
	)
	website_type_choices = [
		(1, 'Administración Pública/Institucional'),
		(2, 'Banca Electronica'),
		(3, 'Blog'),
		(4, 'Buscador'),
		(5, 'Comercio electrónico'),
		(6, 'Comunicación/Noticias'),
		(7, 'Corporativo/Empresa'),
		(8, 'Descargas'),
		(9, 'Educativo/Formativo'),
		(10, 'Entornos colaborativos/Wikis'),
		(11, 'Foros/Chat'),
		(12, 'Ocio/Entretenimiento'),
		(13, 'Personal'),
		(14, 'Portal de Servicios'),
		(15, 'Servicios interactivos basados en imágenes'),
		(16, 'Servicios interactivos no basados en imágenes'),
		(17, 'Webmail/Correo')
	]
	website_type = forms.ChoiceField(
		required = True,
		label = 'Tipo de sitio web',
		choices = website_type_choices
	)
	browser_name = forms.CharField(
		required = True,
		label = 'Explorador Usado',
		max_length = 20,
		widget = forms.TextInput({"placeholder": "Ej. Google Chrome"})
	)
	browser_version = forms.CharField(
		required = True,
		label = 'Versión del explorador',
		max_length = 10,
		widget = forms.TextInput({"placeholder": "Ej. 66"})
	)

class HorizontalRadioRenderer(forms.RadioSelect):
   def render(self):
     return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
	
class ReviewItemsForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(ReviewItemsForm, self).__init__(*args, **kwargs)
		quantitative_choices = [('1', '1'), ('2', '2'), ('3', '3'),
								('4', '4'), ('5', '5'), ('6', '6'),
								('7', '7'), ('8', '8'), ('9', '9'), 
								('10', '10'), ('NA', 'NA')
								]
		qualitative_chices = [('NA', 'NA'), ('NTS', 'NTS'), ('NEP', 'NEP'),
							  ('NPP', 'NPP'), ('NPI', 'NPI'), ('S', 'S')
							  ]
							  
		heuristics = MetaHeuristic.objects.all()
		for i in range(0, len(heuristics)):
			
			# Hidden field with heuristic information
			attrs = {'heuristic' : True,
					 'number' : i,
					 'pk' : heuristics[i].pk
					}
			self.fields['H_'+str(heuristics[i].pk)] = forms.CharField(
				required = False,
				label = heuristics[i].name,
				widget = forms.HiddenInput(attrs=attrs)
			)
			criteria = MetaCriteria.objects.filter(heuristic = heuristics[i])
			for j in range(0, len(criteria)):
				
				# Field for each criteria
				if(criteria[j].atribute == 'cualitativo'):
					choices = qualitative_chices
					initial_value = 'S'
				else:
					choices = quantitative_choices
					initial_value = '1'

				self.fields['H_'+str(heuristics[i].pk)+'_C_'+str(criteria[j].pk)] = forms.ChoiceField(
					required = True,
					label = criteria[j].name,
					choices = choices,
					initial = initial_value,
					#widget = forms.RadioSelect(attrs = {'heuristic' : heuristics[i].pk}),
					widget = forms.RadioSelect(),
				)
			
			# Hidden field to identify the ending of an heuristic's criteria
			self.fields['H_'+str(heuristics[i].pk)+'_END'] = forms.CharField(
				required = False,
				label = heuristics[i].name,
				widget = forms.HiddenInput(attrs={'heuristic_end' : True})
			)
				
class MetaHeuristicForm(forms.Form):
	name = forms.CharField(
		required = True,
		label = 'Nombre',
		max_length = 100,
		min_length = 10,
		widget = forms.TextInput({"placeholder": "Ej. Aspectos Generales"})
	)
	acronym = forms.CharField(
		required = True,
		label = 'Acrónimo',
		max_length = 2,
		min_length = 1,
		widget = forms.TextInput({"placeholder": "Ej. AG"})
	)
	
class MetaCriterionForm(forms.Form):
	heuristic = forms.ModelChoiceField(
		required = True,
		label = 'Heuristica',
		empty_label = 'Seleccione uno',
		queryset=MetaHeuristic.objects.all()
	)
	name = forms.CharField(
		required = True,
		label = 'Nombre',
		max_length = 100,
		min_length = 10,
		widget = forms.TextInput({"placeholder": "Ej. Objetivos bien definidos"})
	)
	acronym = forms.CharField(
		required = True,
		label = 'Acrónimo',
		max_length = 3,
		min_length = 1,
		widget = forms.TextInput({"placeholder": "Ej. AG1"})
	)
	atribute = forms.ChoiceField(
		required = True,
		label = 'Atributo',
		choices = [('cualitativo', 'cualitativo'), ('cuantitativo', 'cuantitativo')],
		initial = 'cualitativo',
	)
	metric = forms.CharField(
		required = True,
		label = 'Métrica',
		max_length = 12,
		widget = forms.TextInput({"placeholder": "Ej. - "})
	)
	
class FilterMetaCriteriaForm(forms.Form):
	heuristic = forms.ModelChoiceField(
		required = False,
		label = 'Heuristica',
		empty_label = 'Todos',
		queryset=MetaHeuristic.objects.all()
	)
		
	
	
	
	
