from django.db import models
from employer.models import EmployerModel


# Create your models here.
class ClientModel(models.Model):
    nomCompletClient = models.CharField(max_length=50, verbose_name='Nom')
    telephoneClient = models.CharField(max_length=12, primary_key=True, unique=True, verbose_name='Téléphone')
    emailClient = models.EmailField(max_length=254, unique=True, verbose_name='E-mail')
    employerContacter = models.ForeignKey(EmployerModel, on_delete=models.CASCADE, verbose_name='Employer concerner')

    def __str__(self):
        return self.nomCompletClient

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
