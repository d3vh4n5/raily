from django import forms
from .models import Sender

# class SenderForm(forms.ModelForm):
#     class Meta:
#         model = Sender
#         fields = ['name', 'email']  # Los campos del formulario que deseas incluir

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  # Recuperar el usuario del argumento de palabras clave
#         super(SenderForm, self).__init__(*args, **kwargs)
#         if user:
#             self.fields['user'] = user  # Establecer el usuario como valor inicial para el campo 'user'

class SenderForm(forms.Form):
    name = forms.CharField(max_length=50, label='Name', required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(max_length=128, label='Password', required=True)