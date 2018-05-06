from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    full_name = forms.CharField(
        required = True,
        label = 'Full name',
        max_length = 60
    )
    telephone= forms.CharField(
        required = False,
        label = 'Telephone',
        max_length = 11
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )

