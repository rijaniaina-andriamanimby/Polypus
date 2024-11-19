from django.urls import path
from .views import *


urlpatterns = [
    path('', index_villa_u, name='listVillaU'),
    path('ajouter/', add_villa_u, name='ajouterDesVillasU'),
    path('modifier/<str:lotVilla>', update_villa_u, name='modifierUnVillaU'),
    path('supprimer/<str:lotVilla>', delete_villa_u, name='supprimerUnVillaU'),
    ]
