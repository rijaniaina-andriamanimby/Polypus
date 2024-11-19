from django.urls import path
from .views import *


urlpatterns = [
    path('', index_ville, name='listVille'),
    path('ajouter/', add_ville, name='ajouterDesVilles'),
    path('modifier/<str:codePostal>', update_ville, name='modifierUneVille'),
    path('supprimer/<str:codePostal>', delete_ville, name='supprimerUnVille'),
]
