from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import User
import datetime


class UserRegistrationForm(forms.Form):
    user = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
        widget = forms.TextInput({"placeholder": "Username"})

    )
    full_name = forms.CharField(
        required = True,
        label = 'Full name',
        max_length = 60,
        widget = forms.TextInput({"placeholder": "Full Name"})

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
        widget = forms.TextInput({"placeholder": "Email"})
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput({"placeholder": "Password"})
    )
    
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
	
	
	
