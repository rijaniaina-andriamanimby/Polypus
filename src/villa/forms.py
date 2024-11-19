from django import forms
from .models import VillaModel, ImageModel


class VillaForm(forms.ModelForm):
    class Meta:
        model = VillaModel
        fields = ['nomVilla', 'details', 'descriptionVilla' ]
        labels = {
            'nomVilla': 'Nom du villa :',
            'details': 'Détails',
            'descriptionVilla': 'Description :',
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image', 'villaConcerner']
        labels = {
            'image': 'Votre image',
            'villaConcerner': 'Villa'
        }
