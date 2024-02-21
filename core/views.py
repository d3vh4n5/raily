from django.shortcuts import render
from .forms import RegistrarUsuarioForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    context= {}
    return render(request, 'core/pages/index.html', context)


def user_register(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente.")
            return render(request, 'core/pages/register.html')
            # return redirect('my_login')
    else:
        form = RegistrarUsuarioForm()
    
    context = {
        'form' : form,
        'title' : 'Login'
    }
    
    return render(request, 'core/pages/register.html', context)

@login_required
def profile(request):
    return render(request, 'core/pages/profile.html')