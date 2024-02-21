from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegistrarUsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingrese una dirección de correo electrónico válida.')
    first_name = forms.CharField(max_length=30, help_text='Requerido. Ingrese su nombre.')
    last_name = forms.CharField(max_length=30, help_text='Requerido. Ingrese su apellido.')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso. Por favor, elija otro.')
        return email
