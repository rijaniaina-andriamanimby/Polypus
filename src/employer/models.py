from django.db import models


# Create your models here.
class EmployerModel(models.Model):
    matriculeEmployer = models.CharField(max_length=10, primary_key=True, unique=True, verbose_name='Matricule')
    nomPrenomsEmployer = models.CharField(max_length=100, verbose_name='Nom')
    emailEmployer = models.EmailField(max_length=50, unique=True, verbose_name='E-mail')
    adresseEmployer = models.CharField(max_length=50, verbose_name='Adresse')
    fonctionEmployer = models.CharField(max_length=32, verbose_name='Fonction')

    def __str__(self):
        return self.nomPrenomsEmployer

    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'
