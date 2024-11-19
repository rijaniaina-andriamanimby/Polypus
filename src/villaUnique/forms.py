from django import forms
from .models import VillaUnique


class VillaFormU(forms.ModelForm):
    class Meta:
        model = VillaUnique
        fields = ['lotVilla', 'modelVilla', 'prix']
