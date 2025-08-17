from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)
urlpatterns = [
     path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # Added for prompt
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Added for prompt
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-edit'),  # Added for prompt
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Added for prompt
     path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-add'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),# The previous plural 'posts/' routes can be kept for compatibility if needed
]





