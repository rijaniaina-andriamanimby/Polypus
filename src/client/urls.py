from django.urls import path
from .views import index_client, list_client, add_client, update_client, delete_client, client_reserver

urlpatterns =[
    path('', list_client, name="listDesClient"),
    path('client_reserver/', client_reserver, name='listClientReserver'),
    path('ajouter/', add_client, name="ajouterDesClients"),
    path('modifier/<str:telephoneClient>', update_client, name="modifierUnClient"),
    path('supprimer/<str:telephoneClient>', delete_client, name="supprimerUnClient"),
]
