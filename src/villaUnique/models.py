from django.db import models
from villa.models import VillaModel


# Create your models here.
class VillaUnique(models.Model):
    lotVilla = models.CharField(max_length=32, primary_key=True, verbose_name="Lot du villa")
    modelVilla = models.ForeignKey(VillaModel, on_delete=models.CASCADE, verbose_name="Modèle du villa")
    prix = models.FloatField()

    def __str__(self):
        return self.lotVilla

    class Meta:
        verbose_name = "Villa unique"
        verbose_name_plural = "Villas uniques"
