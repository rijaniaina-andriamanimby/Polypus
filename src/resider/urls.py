from django.urls import path
from .views import *


urlpatterns = [
    path('', index_residence, name='listResidence'),
    path('ajouter/', add_residence, name='ajouterDesResidence'),
    path('modifier/<int:id>', update_residence, name='modifierUneResidence'),
    path('supprimer/<int:id>', delete_residence, name='supprimerUnResidence'),
]
