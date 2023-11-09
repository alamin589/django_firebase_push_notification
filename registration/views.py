from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm, LoginForm
import firebase_admin
from firebase_admin import credentials, messaging
from django.http import JsonResponse
from django.http import HttpResponse
cred = credentials.Certificate("/home/alamin/Downloads/fir-notification-1a046-firebase-adminsdk-uh2jp-c59187320e.json")
firebase_admin.initialize_app(cred)

def send_notification_to_user(fcm_token, username, title, body, sender_username):
    if fcm_token:
        message = messaging.Message(
            notification=messaging.Notification(title=f'{username}: {title}', body=body),
            token=fcm_token,
        )
        try:
            response = messaging.send(message)
            print(f"Notification sent successfully to user {username} from {sender_username}: {response}")
        except Exception as e:
            print("Error sending notification to token:", fcm_token)
            print("Error details:", e)


def send_notification_to_all_users(title, body, sender_username):
    fcm_tokens_and_usernames = User.objects.filter(fcm_token__isnull=False).values_list('fcm_token', 'username')
    for fcm_token, username in fcm_tokens_and_usernames:
        send_notification_to_user(fcm_token, username, title, body, sender_username)

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            fcm_token = request.POST.get('fcm_token')

            user = User(username=username, password=password, fcm_token=fcm_token)
            user.save()
            return JsonResponse({'message': 'Registration successful'})
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username, password=password).first()
            if user:
                send_notification_to_user(user.fcm_token, username, "User logged in", f"User logged in: {username}", sender_username=username)  # Change sender_username here

                send_notification_to_all_users("User logged in", f"User logged in: {username}", sender_username=username)  # Change sender_username here

                return JsonResponse({'message': 'Login successful'})
            else:
                pass
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyB6jQo8ZTK9zozcrBLeUEhr8b0VqW8wzIg",' \
           '        authDomain: "fir-notification-1a046.firebaseapp.com",' \
           '        databaseURL: "https://fir-notification-1a046-default-rtdb.asia-southeast1.firebasedatabase.app",' \
           '        projectId: "fir-notification-1a046",' \
           '        storageBucket: "fir-notification-1a046.appspot.com",' \
           '        messagingSenderId: "37413689044",' \
           '        appId: "1:37413689044:web:3e2f4ac0758af5f8048d41",' \
           '        measurementId: "G-28CQ98BKMV"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging = firebase.messaging();' \
           'messaging.onBackgroundMessage(function (payload) {' \
           '    console.log(payload);' \
           '    const notification = payload;' \
           '    const notificationOptions = {' \
           '        body: notification.data.body,' \
           '        icon: notification.data.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title, notificationOptions);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")