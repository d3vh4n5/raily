from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os
from datetime import datetime
from raily_api.utils.uainfo import analizar_user_agent
from .models import Visit
from .serializers import VisitSerializer
from django.contrib.auth.models import User

load_dotenv()


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_visit(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    origin= request.data["origin"]
    
    if not ip:
        ip = request.META.get('REMOTE_ADDR')

    try:
        avoid_ip = os.environ["AVOID_IP"]

        if ip == avoid_ip or ip == '127.0.0.1':
            return Response({"detail": "Visit avoided"})
        # Evitar el IP

        api_key = os.environ["IPINFO_API_KEY"]
        url = f"https://ipinfo.io/{ip}?token={api_key}"
        resp = requests.get(url)
        data = resp.json()
        user = User.objects.get(username=request.user)


        visit = Visit(
            user = user,
            tag = 'Test Tag',
            origin = origin,
            date = datetime.now(),
            agent = request.META.get('HTTP_USER_AGENT'),
            ip = ip,
            hostname = "test",
            city = data['city'],
            region = data['region'],
            loc = data['loc'],
            org = data['org'],
            postal = data['postal'],
            timezone = data['timezone'],
        )

        visit.save()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return Response({"error" : http_err})
    except Exception as err:
        print(f"Other error occurred: {err}")
        return Response({"error" : err})
    else:
        print("Success!")
        print(data)
        return Response(data)
