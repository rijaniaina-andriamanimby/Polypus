from django import forms
from .models import VilleModel


class VilleForm(forms.ModelForm):
    class Meta:
        model = VilleModel
        fields = ['codePostal', 'nomVille', 'image']
        labels = {
            'codePostal': 'Code postal',
            'nomVille': 'Ville',
            'image': 'Plan de masse'
        }
