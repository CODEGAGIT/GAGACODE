from django import forms
from .models import Suggestion,Billet
from companyman.models import InfoLigne
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .functions import liste_infoligne,liste_ville
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import phonenumbers
import datetime


id=Billet.objects.values_list('id',flat=True).order_by('-id').first()
id_billet=id+1
# Extraire les valeurs des champs 'field1' et 'field2' sous forme de liste de tuples
infolignes = InfoLigne.objects.filter(date_dep__gt=datetime.datetime.now()).values_list(
            'date_dep',
            'bus_id_id',
            'ligne_id_id',
            # 'ligne_id.ville_arr.nom_ville',
            'prix',
            )
# Aplatir la liste de tuples en une liste à plat
flat_values = [value for tuple_value in infolignes for value in tuple_value]
# Créer une liste de tuples contenant les valeurs des champs 'field1' et 'field2'
values = InfoLigne.objects.filter(date_dep__gt=datetime.datetime.now()).values_list(
            'date_dep',
            'bus_id_id',
            'ligne_id_id',
            # 'ligne_id.ville_arr.nom_ville',
            'prix',
            )

# Créer une liste de tuples à partir de la liste de valeurs, en utilisant une compréhension de liste
choices = [(value[0], value[1]) for value in values]

destinataires=[
    ('Plateforme','La Plateforme'),
    ('Nagode', 'Compagnie Nagode'),
    ('Cheval Blanc', 'Compagnie Cheval Blanc'),
    ('Rakieta', 'Compagnie Rakieta'),
    ('LK', 'Compagnie LK'),
    ('ETRAB', 'Compagnie ETRAB'),
    ('Adji Transport', 'Compagnie Adji Transport'),
    ('DC10', 'Compagnie DC10')
]


class SuggestionForm(forms.ModelForm):
    class Meta:
        model=Suggestion
        fields=('email','destinataire','message')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input100', 'placeholder':'Email'}),
            'destinataire': forms.Select(attrs={'class': 'input100', 'placeholder':'Destiné à'}, choices=destinataires), 
            'message': forms.Textarea(attrs={'class': 'input100', 'placeholder':'Saisissez Votre Message...'}),
        }

class BilletForm(forms.Form):
    nom_clt=forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input100', 'placeholder':'Nom'})
        )
    prenom_clt=forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input100', 'placeholder':'Prénom'})
        )
    email_clt=forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input100', 'placeholder':'E-mail'})
        )
    telephone_clt=PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'input100', 'placeholder':'Téléphone'})
        )
    place=forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'input20',
            'min':'1', 
            'max':'5',
            'placeholder':'Place'})
        )
    
class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Envoyer'))

        self.helper.layout = Layout(
            'email',
            'message',
        )
class RechercheBillet(forms.Form):
    code_billet=forms.CharField(widget=forms.TextInput(attrs={'class': 'input100', 'placeholder':'Code'})
        )        
    