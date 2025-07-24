from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Book CRUD operations with permission checks
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Security demonstration views
    path('permissions/', views.user_permissions, name='user_permissions'),
    path('form-example/', views.form_example, name='form_example'),
]
