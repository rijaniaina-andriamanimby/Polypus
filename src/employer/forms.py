from django import forms
from .models import *


class EmployerForm (forms.ModelForm):
    class Meta:
        model = EmployerModel
        fields = ['matriculeEmployer', 'nomPrenomsEmployer', 'emailEmployer', 'adresseEmployer', 'fonctionEmployer']
        labels = {
            'matriculeEmployer': 'Matricule :', 'nomPrenomsEmployer': 'Nom complet :', 'emailEmployer': 'E-mail :',
            'adresseEmployer': 'Adresse :', 'fonctionEmployer': 'Fonction :'
        }