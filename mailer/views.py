from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import SenderForm
from .models import Sender
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

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

    context = {
        'senders': queryset,
        'base_url' : 'http://localhost:8000/'

    }

    return render(request, 'mailer/pages/senders_list.html', context)

@csrf_exempt
def sendMail(request, uid, senderId):

    requestToken = request.GET.get('token', None)
    # requestToken = request.GET['token'] Así también lo obtengo pero no puedo validar

    if requestToken == None:
        return HttpResponse("Token incorrecto")
    

    if request.method == 'POST':
        try:
            user = User.objects.get(id=uid)
            sender = Sender.objects.get(id=senderId)

            print(requestToken)
            print(user)
            data = json.loads(request.body)


            resp = {
                'userName' : user.username,
                'senderName' : sender.name,
                "senderEmail": sender.email,
                "senderPass": sender.password,
                "mailTo" : data.get("mailTo"),
                "subject" : data.get("subject"),
                "content" : data.get("content"),
            }

            print(resp)

            return JsonResponse(resp)
        except Exception as e:
            print('Hubo un error al obtener la información', e)
    
    return HttpResponse('Nothing to show')