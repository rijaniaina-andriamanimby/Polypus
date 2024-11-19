from django.urls import path
from .views import *

urlpatterns = [
    # path('', acceuil_publication, ),
    path('a_propos/', a_propos, name="aproposPublication"),
    path('detail_projet/<str:nomVille>', projet_detail, name="projetDetailPublication"),
    path('technologies/', technologies, name="technologiesPublication"),
    path('contact/', contact, name="contactPublication"),
    path('reservation/', reservation, name="reservationPublication"),
    path('reservation/', reservation, name="reservationPublication2"),
    path('get-lots/', get_lots, name='get_lots'),
    path('get-villas/', get_villa_model, name='get_villa_model'),
]
