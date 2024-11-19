from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index_villa, name='listVilla'),
    path('ajouter/', add_villa, name='ajouterDesVillas'),
    path('modifier/<int:lotVilla>', update_villa, name='modifierUnVilla'),
    path('supprimer/<int:lotVilla>', delete_villa, name='supprimerUnVilla'),
    path('image_villa/', index_image, name='listImage'),
    path('ajouter_villa/', add_image, name='ajouterDesImages'),
    path('modifier_villa/<int:id>', update_image, name='modifierUneImage'),
    path('supprimer_villa/<int:id>', delete_image, name='supprimerUneImage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
