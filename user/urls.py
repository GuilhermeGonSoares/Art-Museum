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
    path('edit/', views.edit_user, name='edit'),
    path('painting/create/', views.painting_create, name='painting_create'),
    path('painting/published/', views.painting_user_published, name='paintings_published'),
    path('author/create/', views.painting_author_create, name='painting_author_create'),
    path('church/create/', views.painting_church_create, name='painting_church_create'),
    path('engraving/all/', views.engravings, name= 'painting_engraving_all'),
    path('engraving/create/', views.engraving_create, name='painting_engraving_create'),
    path('engraving/create/data/', views.engraving_create_data, name='engraving_create_data'),
    path('painting/<int:id>/delete/', views.painting_delete, name='painting_delete'),
    path('painting/<int:id>/edit/', views.painting_edit, name='painting_edit'),
]
