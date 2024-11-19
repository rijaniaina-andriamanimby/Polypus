from django import forms
from .models import ClientModel


class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['nomCompletClient', 'telephoneClient', 'emailClient',
                  'employerContacter'
                  ]
        labels = {
            'nomCompletClient': 'Nom et prénoms ', 'telephoneClient': 'Téléphone ',
            'emailClient': 'E-mail ',
            'employerContacter': 'Personnel contacter',
        }

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['nomCompletClient'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['telephoneClient'].widget.attrs.update({'placeholder': 'Numéro de téléphone'})
    #     self.fields['emailClient'].widget.attrs.update({'placeholder': 'E-mail'})
    #     self.fields['adresseClient'].widget.attrs.update({'placeholder': 'Adresse du client'})
    #     self.fields['interestedClient'].widget.attrs.update({'placeholder': 'Intérêt du client ?'})
    #     self.fields['fonctionClient'].widget.attrs.update({'placeholder': 'Fonction du client'})
    #     self.fields['fonctionClient'].widget.attrs.update({'class': 'form-select'})


class ClientRechercheForm(forms.ModelForm):
    recherche = forms.CharField(max_length=32)