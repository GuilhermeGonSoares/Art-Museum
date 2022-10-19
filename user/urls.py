from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('painting/create/', views.painting_create, name='painting_create'),
    path('painting/author/create/', views.painting_author_create, name='painting_author_create'),
    path('painting/church/create/', views.painting_church_create, name='painting_church_create'),
    path('painting/<int:id>/delete/', views.painting_delete, name='painting_delete'),
    path('painting/<int:id>/edit/', views.painting_edit, name='painting_edit'),
]
