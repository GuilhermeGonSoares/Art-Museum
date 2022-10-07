from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/create/', views.register_create, name='create')
]
