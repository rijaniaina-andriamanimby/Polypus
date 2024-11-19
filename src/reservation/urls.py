from django.urls import path
from .views import index_reservation, add_update_reservation, delete_reservation, rapport

urlpatterns =[
    path('', index_reservation, name='listReservation'),
    path('ajouter/', add_update_reservation, name='ajouterDesReservations'),
    path('modifier/<int:id>', add_update_reservation, name='modifierUnReservation'),
    path('supprimer/<int:id>', delete_reservation, name='supprimerUnReservation'),
    path('rapport/', rapport, name='rapportReservation')
]
