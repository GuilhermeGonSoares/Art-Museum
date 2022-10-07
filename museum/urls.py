from django.urls import path

from museum import views

app_name = 'painting'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('painting/<int:painting_id>/', views.detail_painting, name='detail'),
    path('church/<int:id_church>/', views.detail_church, name='church'),
    path('painter/<int:id_painter>/', views.detail_painter, name='painter'),
]