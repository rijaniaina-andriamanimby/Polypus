from django.db import models
from ville.models import VilleModel
from villa.models import VillaModel


# Create your models here.
class Resider(models.Model):
    villeVilla = models.ForeignKey(VilleModel, on_delete=models.CASCADE, verbose_name="Emplacement", related_name="ville")
    villaModel = models.ForeignKey(VillaModel, on_delete=models.CASCADE, verbose_name="Modèle", related_name="villa")
