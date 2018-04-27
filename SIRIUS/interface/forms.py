from django import forms

class TestForm(forms.Form):
	name = forms.CharField(label='Nombre', max_length=100)
	lastname = forms.CharField(label='Apellido', max_length=100)
	age = forms.IntegerField(label='Edad', min_value=0, max_value=200)
