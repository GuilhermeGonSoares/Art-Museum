from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from museum import views

app_name = 'painting'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('church/all/', views.churches, name='church_all'),
    path('painter/all/', views.painters, name='painter_all'),
    path('engraving/all/', views.engravings, name='engraving_all'),
    path("paintings/tag/<slug:slug>/", views.tags_paintings, name="tag"),
    path('painting/<int:painting_id>/', views.detail_painting, name='detail'),
    path('church/<int:id_church>/', views.detail_church, name='church'),
    path('painter/<int:id_painter>/', views.detail_painter, name='painter'),
    path('engraving/<int:id_engraving>/', views.detail_engraving, name='engraving'),
    path('user/dashboard/painting/<int:painting_id>/', views.detail_painting_not_published, name='detail_not_published'),
    path('info/', views.info, name='info'),
]

urlpatterns += staticfiles_urlpatterns()