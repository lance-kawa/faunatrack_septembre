from django import forms
import logging
from faunatrack.models import Coordonnee, Observation, Projet, Scientifique

logger = logging.getLogger()

class FaunaTrackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FaunaTrackForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'border rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5'


class ScientifiqueForm(FaunaTrackForm):
    class Meta:
        model = Scientifique
        fields = ["user", "role"]

class ProjetForm(FaunaTrackForm):
    class Meta:
        model = Projet
        fields = ["titre", "description", "scientifique",]

    notes = forms.CharField()
    scientifique = ScientifiqueForm()

    def clean_titre(self):
        logger.warning("titre est en cours de vérif!")
        titre = self.cleaned_data.get("titre", None) # /!\ Toujours récupérer les données depuis le dico cleaned_data pour éviter les mauvais surprises
        if "pabo" in titre:
            raise forms.ValidationError("Votre titre doit être plus beau que ça !")
        return titre



class ObservationForm(FaunaTrackForm):
    class Meta:
        model = Observation
        fields = [ 'espece',  'date', 'quantite', 'notes']
        widgets = {
            'date': forms.widgets.DateInput( 
                attrs={
                    'type': 'date',
                }
            ),
        }
    quantite = forms.IntegerField(
        label="Quantité",
        help_text="Nombre d'individus observés",
        min_value=1,
        max_value=1000, # Navigateur
    )
    coordonnee = forms.ModelChoiceField(queryset=Coordonnee.objects.all())

    # Mot clef django clean_<nom_du_champ>
    def clean_quantite(self): # Serveur Web
        quantite = self.cleaned_data.get('quantite', None) 
        if quantite > 1000 or quantite < 1:
            raise forms.ValidationError("Quantite incorrect")
        return quantite

