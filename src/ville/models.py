import os

from django.db import models
from django.dispatch import receiver


# Create your models here.
class VilleModel(models.Model):
    codePostal = models.CharField(max_length=5, primary_key=True, verbose_name="Code postale")
    nomVille = models.CharField(max_length=32, verbose_name="Nom du ville")
    image = models.ImageField(upload_to='images/', null=False, blank=False)

    def __str__(self):
        return self.nomVille

    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"


@receiver(models.signals.post_delete, sender=VilleModel)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Supprime le fichier image du disque après suppression de l'objet en base de données.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
