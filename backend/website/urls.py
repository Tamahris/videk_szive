from django.urls import path
from . import views

urlpatterns = [
    path('', views.fooldal_view, name='fooldal'), 
    path('szallas/', views.szallas_view, name='szallas'),
    path('wellness/', views.wellness_view, name='wellness'),
    path('etterem/', views.etterem_view, name='etterem'),
    path('galeria/', views.galeria_view, name='galeria'),
    path('kapcsolat/', views.kapcsolat_view, name='kapcsolat'),
    path('foglalas/', views.foglalas_view, name='foglalas'),
]