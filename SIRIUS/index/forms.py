from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
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
    email = forms.CharField(
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

