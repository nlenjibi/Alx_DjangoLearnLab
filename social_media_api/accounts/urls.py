from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from rest_framework.authtoken import views as drf_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/', drf_views.obtain_auth_token, name='api_token_auth'),
]
