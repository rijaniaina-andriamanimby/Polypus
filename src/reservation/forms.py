from django import forms
from .models import ReservationModel


class CalendarWidget(forms.TextInput):
    class Media:
        js = ["jQuery.js", "calendar.js", "noConflict.js"]


class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReservationModel
        fields = ['villaReserver', 'clientReserver', 'lotReserver', 'dateReservation', 'accompte']
        labels = {
            'villaReserver': 'Villa :', 'clientReserver': 'Client :',
            'lotReserver': 'Lotissement :'
            , 'dateReservation': 'Date de réservation :', 'accompte': 'Accompte de 30 %'
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['dateReservation'].widget.attrs.update({'placeholder': 'dd/mm/YYYY'})
