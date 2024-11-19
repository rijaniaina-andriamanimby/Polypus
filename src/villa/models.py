import os
from django.db import models
from django.dispatch import receiver
from employer.models import EmployerModel
from ville.models import VilleModel


# Create your models here.
class VillaModel(models.Model):
    # lotVilla = models.CharField(max_length=32, primary_key=True, unique=True, verbose_name='Lotissement')
    lotVilla = models.AutoField(primary_key=True, verbose_name='Code villa')
    nomVilla = models.CharField(max_length=32, verbose_name='Nom du villa')
    details = models.ImageField(upload_to="images/")
    descriptionVilla = models.TextField(verbose_name='Description')

    def __str__(self):
        return self.nomVilla

    class Meta:
        verbose_name = 'Villa'
        verbose_name_plural = 'Villas'


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    villaConcerner = models.ForeignKey(VillaModel, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


# Signal pour supprimer l'image après suppression de l'enregistrement
@receiver(models.signals.post_delete, sender=ImageModel)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Supprime le fichier image du disque après suppression de l'objet en base de données.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
