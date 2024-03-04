from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import SenderForm
from .models import Sender, ApiKey
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
import datetime
# from mailer.utils.automail import sendAutoMail

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
    try:
        hasApiKey = ApiKey.objects.get(user=request.user)
        api_key = hasApiKey.value
    except Exception as e:
        hasApiKey = False
        api_key = '<yourapikeyhere>'
        print("La key no se encontro, procedemos a crear una nueva")

    user = request.user
    queryset = Sender.objects.filter(user=user)

    context = {
        'senders': queryset,
        'base_url' : 'http://localhost:8000/',
        'api_key' : api_key,
    }

    return render(request, 'mailer/pages/senders_list.html', context)

@csrf_exempt
def sendMail(request, uid, senderId):

    requestToken = request.GET.get('apikey', None)
    # requestToken = request.GET['token'] Así también lo obtengo pero no puedo validar
    
    # Verificar el token y en usuario en la db

    if requestToken == None:
        return HttpResponse("Debe incluir una api key para poder hacer uso de la api")
    
    try:
        userKey = ApiKey.objects.get(value=requestToken)
        # print(userKey.user)
        # print(request.user)
        # Aqui en realidad se debe verificar una atenticación del usuario
    except Exception as e:
        return HttpResponse("Clave incorrecta")

    if request.method == 'POST':
        try:
            user = User.objects.get(id=uid)
            sender = Sender.objects.get(id=senderId)

            data = json.loads(request.body)

            resp = {
                'userName' : user.username,
                "senderEmail": sender.email,
                "mailTo" : data.get("mailTo"),
                "subject" : data.get("subject"),
                "content" : data.get("content"),
            }

            # print(resp)

            # sendAutoMail(
            #     sender.email,
            #     sender.password,
            #     data.get("mailTo"),
            #     data.get("subject"),
            #     data.get("content")
            # )

            return JsonResponse(resp)
        except Exception as e:
            print('Hubo un error al obtener la información', e)
            return HttpResponse('Hubo un error al obtener la información')
    
    return HttpResponse('Nothing to show')

@login_required
def create_api_key(request):
    try:
        hasApiKey = ApiKey.objects.get(user=request.user)
        print(hasApiKey)
    except Exception as e:
        hasApiKey = False
        print("La key no se encontro, procedemos a crear una nueva")

    if not hasApiKey:
        date = str(datetime.datetime.now())
        userName = str(request.user)
        encodedVars = (userName + date).encode('utf8')
        hash = hashlib.sha256(encodedVars).hexdigest()


        try:
            newApiKey = ApiKey(
                user = request.user,
                value = hash
            )

            newApiKey.save()

            return redirect('senders_list')
        
        except Exception as e:
            print(e)
            return HttpResponse("Ocurrió un error al crear la api key, por favor comuníquese con el desarrollador.")

    else:
        return HttpResponse("Usuario ya tiene api key")
