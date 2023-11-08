# views.py
from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm, LoginForm
import firebase_admin
from firebase_admin import credentials, messaging
from django.http import JsonResponse

# Initialize Firebase Admin SDK (you should have the JSON key file)
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

            # Generate FCM token
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
                # You can add authentication logic here, like setting session variables.

                # Send a login notification to the user who is logging in
                send_notification_to_user(user.fcm_token, username, "User logged in", f"User logged in: {username}", sender_username=username)  # Change sender_username here

                # Send a login notification to all users
                send_notification_to_all_users("User logged in", f"User logged in: {username}", sender_username=username)  # Change sender_username here

                return JsonResponse({'message': 'Login successful'})
            else:
                # Handle invalid login credentials, e.g., displaying an error message.
                pass
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})





# # views.py
# from django.shortcuts import render, redirect
# from .models import User
# from .forms import RegistrationForm, LoginForm
# import string
# from django.shortcuts import render
# from django.http import JsonResponse
# import random
# import firebase_admin
# from firebase_admin import credentials, messaging
# from django.conf import settings

# # Initialize Firebase Admin SDK (you should have the JSON key file)
# cred = credentials.Certificate("/home/alamin/Downloads/fir-notification-1a046-firebase-adminsdk-uh2jp-c59187320e.json")
# firebase_admin.initialize_app(cred)


# # def generate_fcm_token():
# #     # Generate a valid FCM registration token
# #     registration_token = messaging.create_registration_token()
# #     return registration_token
# # def generate_fcm_token():
# #     token_length = 32
# #     characters = string.ascii_letters + string.digits
# #     while True:
# #         token = ''.join(random.choice(characters) for _ in range(token_length))
# #         # Check if the generated token is unique
# #         if not User.objects.filter(fcm_token=token).exists():
# #             return token

# def send_notification_to_all_users(title, body):
#     fcm_tokens = User.objects.filter(fcm_token__isnull=False).values_list('fcm_token', flat=True)
#     for fcm_token in fcm_tokens:
#         if fcm_token:
#             message = messaging.Message(
#                 notification=messaging.Notification(title=title, body=body),
#                 token=fcm_token,
#             )
#             try:
#                 response = messaging.send(message)
#                 print("Notification sent successfully:", response)
#             except Exception as e:
#                 print("Error sending notification to token:", fcm_token)
#                 print("Error details:", e)

# def generate_fcm_token():
#     # Generate an FCM token and return it
#     registration_token = messaging.get_token()
#     return registration_token

# def registration_view(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             # Generate FCM token
#             fcm_token = request.POST.get('fcm_token')

#             user = User(username=username, password=password, fcm_token=fcm_token)
#             user.save()
#             return JsonResponse({'message': 'Registration successful'})
#     else:
#         form = RegistrationForm()

#     return render(request, 'registration.html', {'form': form})

# # def registration_view(request):
# #     if request.method == 'POST':
# #         # Handle the registration form submission
# #         # Save user registration data to the database
# #         # Retrieve the FCM token from the request and store it in the user's profile
# #         fcm_token = request.POST.get('fcm_token')
# #         # Store the FCM token in your database associated with the user

# #         # You can return a JSON response to the client if needed
# #         return JsonResponse({'message': 'Registration successful'})
    
# #     return render(request, 'registration.html')

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = User.objects.filter(username=username, password=password).first()
#             if user:
#                 # You can add authentication logic here, like setting session variables.

#                 # Send a login notification to all users
#                 send_notification_to_all_users("User logged in", f"User logged in: {username}")

#                 return redirect('home')
#             else:
#                 # Handle invalid login credentials, e.g., displaying an error message.
#                 pass
#     else:
#         form = LoginForm()

#     return render(request, 'login.html', {'form': form})


















# # views.py
# from django.shortcuts import render, redirect
# from .models import User
# from .forms import RegistrationForm, LoginForm
# import string
# import random
# import requests
# import json
# from django.http import JsonResponse
# import firebase_admin
# from firebase_admin import credentials, messaging
# from django.conf import settings
# from django.shortcuts import redirect
# import firebase_admin
# from firebase_admin import messaging

# def is_valid_fcm_token(token):
#     fcm_api = "AAAACLYHltQ:APA91bGzBsFKZcCOvS7zmuCIJHxipXkOgnZhbDanaK-DESE_AMq0MenF4uHDSMgO2t-Ia0YJiN0NSrvAJxmejN8-cOqTfl10iqqCpN6M9Ki2qIrdy3BwAwgT4hVEmbx_LwNT27vBTU8V"  # Replace with your FCM API key
#     url = "https://fcm.googleapis.com/fcm/send"

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": 'key=' + fcm_api
#     }

#     payload = {
#         "registration_ids": [token],  # Use the token you want to verify
#     }

#     result = requests.post(url, data=json.dumps(payload), headers=headers)

#     if result.status_code == 200:
#         try:
#             response_data = result.json()
#             if response_data.get("failure", 0) == 0:
#                 return True  # Token is valid
#             else:
#                 return False  # Token is not valid
#         except json.JSONDecodeError:
#             print("Received a non-JSON response:", result.text)

#     return False  # Token is not valid or an error occurred

# def generate_fcm_token():
#     token_length = 32
#     characters = string.ascii_letters + string.digits
#     while True:
#         token = ''.join(random.choice(characters) for _ in range(token_length))
        
#         if is_valid_fcm_token(token):
#             if not User.objects.filter(fcm_token=token).exists():
#                 return token


# def send_notification(sender_id, message_title, message_desc, receivers):
#     fcm_api = "AAAACLYHltQ:APA91bGzBsFKZcCOvS7zmuCIJHxipXkOgnZhbDanaK-DESE_AMq0MenF4uHDSMgO2t-Ia0YJiN0NSrvAJxmejN8-cOqTfl10iqqCpN6M9Ki2qIrdy3BwAwgT4hVEmbx_LwNT27vBTU8V"  # Replace with your FCM API key
#     url = "https://fcm.googleapis.com/fcm/send"

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": 'key=' + fcm_api
#     }

#     valid_tokens = []
#     for receiver in receivers:
#         try:
#             registration_info = messaging.get_registration_token_info(receiver)
#             if registration_info.is_valid:
#                 valid_tokens.append(receiver)
#         except ValueError:
#             # Handle any exceptions that may occur during token validation
#             continue

#     if not valid_tokens:
#         return JsonResponse({'error': 'No valid tokens found'})

#     payload = {
#         "registration_ids": valid_tokens,
#         "data": {
#             "title": message_title,
#             "body": message_desc,
#             "sender_user_id": sender_id,
#         }
#     }

#     result = requests.post(url, data=json.dumps(payload), headers=headers)

#     if result.status_code == 200:
#         try:
#             response_data = result.json()
#             print(response_data)
#         except json.JSONDecodeError:
#             print("Received a non-JSON response:", result.text)
#     else:
#         print("Received a non-200 status code:", result.status_code)

# def registration_view(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             fcm_token = generate_fcm_token()
#             user = User(username=username, password=password, fcm_token=fcm_token)
#             user.save()
#             return redirect('login')
#     else:
#         form = RegistrationForm()

#     return render(request, 'registration.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = User.objects.filter(username=username, password=password).first()
#             if user:
#                 # User logged in successfully, set session variables if needed.

#                 # Retrieve the list of FCM tokens from the database
#                 fcm_tokens = User.objects.values_list('fcm_token', flat=True).filter(fcm_token__isnull=False)
#                 receivers = list(fcm_tokens)

#                 # Send a login notification to all users
#                 send_notification(user.user_id, "User logged in", f"User logged in: {username}", receivers)

#                 return redirect('/')  # Replace 'home' with your home page URL
#     else:
#         form = LoginForm()

#     return render(request, 'login.html', {'form': form})


# {% block content %}
#   <h2>Registration</h2>
#   <form method="post">
#     {% csrf_token %}
#     {{ form.as_p }}
#     <button type="submit">Register</button>
#   </form>
# {% endblock %}

# [07/Nov/2023 09:44:13] "GET /admin/jsi18n/ HTTP/1.1" 200 3343
# Forbidden (CSRF token from POST incorrect.): /reg/register/
# [07/Nov/2023 09:44:25] "POST /reg/register/ HTTP/1.1" 403 2518
# Forbidden (CSRF token from POST incorrect.): /reg/register/
# [07/Nov/2023 09:44:29] "POST /reg/register/ HTTP/1.1" 403 2518
# Forbidden (CSRF token from POST incorrect.): /reg/register/
# [07/Nov/2023 09:44:34] "POST /reg/register/ HTTP/1.1" 403 2518