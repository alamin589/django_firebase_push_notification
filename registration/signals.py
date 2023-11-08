# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .views import send_notification_to_user

@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    # Customize the notification message as needed
    title = "User logged in"
    body = f"User logged in: {user.username}"
    sender_username = "YourApp"  # Customize the sender's name
    send_notification_to_user(user.fcm_token, user.username, title, body, sender_username)
