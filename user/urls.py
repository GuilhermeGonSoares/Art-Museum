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
    path('painting/<int:id>/edit/', views.painting_edit, name='painting_edit'),
    path('painting/<int:painting_id>/author/create/', views.painting_author_create, name='painting_author_create'),
]
