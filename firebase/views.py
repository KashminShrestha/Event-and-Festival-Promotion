
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . models import *
from . serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from .serializers import *
import os
import traceback
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import FCMTokens

from django.shortcuts import render


@csrf_exempt
def save_fcm_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            fcm_token = data.get("token")

            if not fcm_token:
                return JsonResponse({"error": "Token is required"}, status=400)

            token, created = FCMTokens.objects.get_or_create(fcm_token=fcm_token)

            if created:
                message = "Token saved successfully"
            else:
                message = "Token already exists"

            return JsonResponse({"message": message}, status=200)

        except Exception as e:
            print("ERROR:", traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def index(request):
    context = {
        "apiKey": os.getenv('apiKey'),
        "authDomain": os.getenv('authDomain'),
        "databaseURL": os.getenv('databaseURL'),
        "projectId": os.getenv('projectId'),
        "storageBucket": os.getenv('storageBucket'),
        "messagingSenderId": os.getenv('messagingSenderId'),
        "appId": os.getenv('appId'),
        "measurementId": os.getenv('measurementId'),
    }
    return render(request, 'notifications.html', context)


def showFirebaseJS(request):
    data = f"""
    importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");
    importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js");
    var firebaseConfig = {{
        apiKey: "{os.getenv('apiKey')}",
        authDomain: "{os.getenv('authDomain')}",
        databaseURL: "{os.getenv('databaseURL')}",
        projectId: "{os.getenv('projectId')}",
        storageBucket: "{os.getenv('storageBucket')}",
        messagingSenderId: "{os.getenv('messagingSenderId')}",
        appId: "{os.getenv('appId')}",
        measurementId: "{os.getenv('measurementId')}"
    }};
    firebase.initializeApp(firebaseConfig);
    const messaging = firebase.messaging();
    messaging.setBackgroundMessageHandler(function (payload) {{
        console.log(payload);
        const notification = payload.notification;
        const notificationOptions = {{
            body: notification.body,
            icon: notification.icon
        }};
        return self.registration.showNotification(payload.notification.title, notificationOptions);
    }});
    """
    return HttpResponse(data, content_type="text/javascript")

