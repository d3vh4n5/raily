from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from mailer.utils.automail import send_auto_mail
from mailer.models import Sender
from mailer.errors.MailSendingError import MailSendingError



# https://www.youtube.com/watch?v=llrIu4Qsl7c&t=368s Auth con django

# https://www.youtube.com/watch?v=xjMP0hspNLE Auth django + react


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        Response({
            "detail": "Not found.",
        },
            status = status.HTTP_404_NOT_FOUND
        )
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({
            'token': token.key,
            'user' : serializer.data
            # 'user' : serializer.data['username']
        })

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'user' : serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    if request.method == 'POST':
        return Response({"resp" : "todo ok"})
    return Response("passed for {}".format(request.user.email))














@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def custom_mail_send(request):

    if request.method == 'POST':
        user = request.user
        sender_id = request.data.get('senderId')
        receiver = request.data.get('mailTo')
        subject = request.data.get('subject')
        body = request.data.get('content')

        if not all([sender_id, receiver, subject, body]):
            return Response({'detail': 'Missing required parameters'}, status=400)

        
        try:
            sender = Sender.objects.get(id=sender_id)
            if sender.user_id != user.id:
                return Response({"detail" : "Sender is invalid"}, status=status.HTTP_400_BAD_REQUEST)
            
            send_auto_mail(
                sender.email,
                sender.password,
                request.data['mailTo'],
                request.data['subject'],
                request.data['content'],
            )

            return Response({"detail" : "Success"}, status=status.HTTP_200_OK)
        except Sender.DoesNotExist:
            return Response({"detail": "Sender not found"}, status=400)
        except MailSendingError as e:
            return Response({"detail": str(e)}, status=500)
            
        
    return Response({'detail' : 'Bad request'}, status=400)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def server_mail_send(request):
    # Este endpoint trabajaría con "resend" un servicio de mails
    pass