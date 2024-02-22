from django.shortcuts import render, redirect, get_object_or_404
from .forms import SenderForm
from .models import Sender
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'mailer/pages/index.html')

@login_required
def create_sender(request):
    if request.method == 'POST':
        form = SenderForm(request.POST)  # Pasar el usuario actual al formulario
        if form.is_valid():

            sender = Sender(
                name = request.POST['name'],
                email = request.POST['email'],
                password = request.POST["password"],
                user = request.user
            )
            try:
                sender.save()
                print("Se guardo correctamente")
            except Exception as e:
                print(e)
            

            return redirect('sender_detail', pk=sender.pk)
    else:
        form = SenderForm()  # Pasar el usuario actual al formulario
    
    return render(request, 'mailer/pages/create_sender.html', {'form': form})
# def create_sender(request):
#     if request.method == 'POST':
#         form = SenderForm(request.POST, user=request.user)  # Pasar el usuario actual al formulario
#         if form.is_valid():
#             sender = form.save()
#             # Redirigir a alguna página de éxito, por ejemplo:
#             return redirect('sender_detail', pk=sender.pk)
#     else:
#         form = SenderForm(user=request.user)  # Pasar el usuario actual al formulario
    
#     return render(request, 'mailer/pages/create_sender.html', {'form': form})

@login_required
def sender_detail(request, pk):
    # Obtener el objeto SenderM o devolver un error 404 si no existe
    sender = get_object_or_404(Sender, pk=pk)

    if sender.user == request.user:
        # Renderizar el template sender_detail.html con el objeto SenderM
        return render(request, 'mailer/pages/sender_detail.html', {'sender': sender})
    else:
        return render(request, 'core/pages/404.html')

@login_required
def senders_list(request):
    user = request.user
    queryset = Sender.objects.filter(user=user)
    print(queryset)

    return render(request, 'mailer/pages/senders_list.html', {'senders': queryset})