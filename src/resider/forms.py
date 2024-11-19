from django import forms
from .models import Resider


class ResiderForm(forms.ModelForm):
    class Meta:
        model = Resider
        fields = ['villeVilla', 'villaModel']
