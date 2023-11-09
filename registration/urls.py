# urls.py
from django.urls import path
from . import views
from .views import registration_view, showFirebaseJS

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    
]
