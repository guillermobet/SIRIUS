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
        label = 'Full name',
        max_length = 60,
        widget = forms.TextInput({"placeholder": "Full Name *"})

    )
    telephone= forms.CharField(
        required = False,
        label = 'Telephone',
        max_length = 11,
        widget = forms.TextInput({"placeholder": "Telephone"})

    )
    email = forms.EmailField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget = forms.TextInput({"placeholder": "Email *"})
    )
    password = forms.CharField(
        required = True,
        label = 'password',
        max_length = 32,
        widget = forms.PasswordInput({"placeholder": "Password *"})
    )
    password_confirmation = forms.CharField(
        required = True,
        label = 'password_confirmation',
        max_length = 32,
        widget = forms.PasswordInput({"placeholder": "Password confirmation *"})
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
		label = 'Evaluator',
		max_length = 60,
		widget = forms.TextInput({"placeholder": "Ex. Maigualida Perez",
								   "readonly": True
								   })
	)
	date = forms.DateField(
		required = True,
		label = 'Evaluation Date',
		initial = datetime.date.today,
	)
	website_name = forms.CharField(
		required = True,
		label = "Website's Name",
		max_length = 100,
		widget = forms.TextInput({"placeholder": "Ex. Google"})
	)
	website_url = forms.URLField(
		required = True,
		label = "Website's URL",
		widget = forms.URLInput({'placeholder': 'Ex. https://www.google.com/'})
	)
	website_description = forms.CharField(
		required = True,
		label = "Website's description",
		widget = forms.TextInput({"placeholder": 'Ex. Search'})
	)
	browser_name = forms.CharField(
		required = True,
		label = 'Broser Name',
		max_length = 20,
		widget = forms.TextInput({"placeholder": "Ex. Google Chrome"})
	)
	browser_version = forms.CharField(
		required = True,
		label = 'Broser Version',
		max_length = 10,
		widget = forms.TextInput({"placeholder": "Ex. 66"})
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
								('10', '10')
								]
		qualitative_chices = [('NA', 'NA'), ('NTS', 'NTS'), ('NEP', 'NEP'),
							  ('NPP', 'NPP'), ('NPI', 'NPI'), ('S', 'S')
							  ]
		
		heuristics = MetaHeuristic.objects.all()
		for i in range(0, len(heuristics)):
			criteria = MetaCriteria.objects.filter(heuristic = heuristics[i])
			for j in range(0, len(criteria)):
				if(criteria[j].atribute == 'qualitative'):
					choices = qualitative_chices
					initial_value = 'NA'
				else:
					choices = quantitative_choices
					initial_value = '1'
					
				self.fields['H_'+str(heuristics[i].pk)+'_C_'+str(criteria[j].pk)] = forms.ChoiceField(
					required = True,
					label = criteria[j].name,
					choices = choices,
					initial = initial_value,
					widget = forms.RadioSelect(attrs = {'heuristic' : heuristics[i].pk}),
				)
				
class AddMetaHeuristicForm(forms.Form):
	name = forms.CharField(
		required = True,
		label = 'Name',
		max_length = 100,
		widget = forms.TextInput({"placeholder": "Ex. Aspectos Generales"})
	)
	acronym = forms.CharField(
		required = True,
		label = 'Acronym',
		max_length = 2,
		widget = forms.TextInput({"placeholder": "Ex. AG"})
	)
	
class AddMetaCriterionForm(forms.Form):
	heuristic = forms.ModelChoiceField(
		required = True,
		label = 'Heuristic',
		queryset=MetaHeuristic.objects.all()
	)
	name = forms.CharField(
		required = True,
		label = 'Name',
		max_length = 100,
		widget = forms.TextInput({"placeholder": "Ex. Objetivos bien definidos"})
	)
	acronym = forms.CharField(
		required = True,
		label = 'Acronym',
		max_length = 3,
		widget = forms.TextInput({"placeholder": "Ex. AG1"})
	)
	atribute = forms.ChoiceField(
		required = True,
		label = 'Attribute',
		choices = [('qualitative', 'qualitative'), ('quantitative', 'quantitative')],
		initial = 'qualitative',
	)
	metric = forms.CharField(
		required = True,
		label = 'Metric',
		max_length = 12,
		widget = forms.TextInput({"placeholder": "Ex. - "})
	)
		
	
	
	
	
