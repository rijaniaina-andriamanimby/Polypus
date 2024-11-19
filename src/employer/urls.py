from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='listEmployer'),
    path('ajouter', employer_formulaire, name='ajouterDesEmployers'),
    path('<str:matriculeEmployer>', update_employer, name="modifierUnEmployer"),
    path('delete/<str:matriculeEmployer>', delete_employer, name="supprimerUnEmployer"),
]
