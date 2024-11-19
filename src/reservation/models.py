from django.db import models
from client.models import ClientModel
from villa.models import VillaModel
from villaUnique.models import VillaUnique


# Create your models here.
class ReservationModel(models.Model):
    villaReserver = models.ForeignKey(VillaModel, on_delete=models.CASCADE, verbose_name='Villa réserver')
    clientReserver = models.ForeignKey(ClientModel, on_delete=models.CASCADE, verbose_name='Client concerner')
    lotReserver = models.ForeignKey(VillaUnique, on_delete=models.CASCADE, verbose_name='Lotissement choisi')
    dateReservation = models.DateField(verbose_name='Date du réservation')
    accompte = models.BooleanField(verbose_name='Escompte de 30%')

    def __str__(self):
        villa = str(self.villaReserver)
        return villa

    class Meta:
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
