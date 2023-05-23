from dashboard.models import Compagnie
from companyman.models import InfoLigne,Ligne,Bus,Ville
import string
import random


villes=Ville.objects.all()
liste_ville=[]
for i in villes:
    liste_ville.append((i.id,i.nom_ville))


    
infolignes = InfoLigne.objects.all()
liste_infoligne = []
for i in infolignes:
    liste_infoligne.append((i.id, i.date_dep))
    
    
# from django.shortcuts import render
# from dashboard.models import Compagnie

# def ma_vue(request):
#     Compagnies = Compagnie.objects.all()
#     ma_liste = []
#     for Compagnie in Compagnies:
#         ma_liste.append((Compagnie.nom, Compagnie.age))
#     contexte = {'liste_Compagnies': ma_liste}
#     return render(request, 'mon_template.html', contexte)

# from django import forms

# class MonFormulaire(forms.Form):
#     choix = forms.ChoiceField(choices=[('Option 1', 'Option 1'), ('Option 2', 'Option 2'), ('Option 3', 'Option 3')], widget=forms.Select())



def code(longueur):
    # Définir les caractères possibles pour le code
    caracteres = string.ascii_letters + string.digits
    # Générer le code alphanumérique
    lecode = ''.join(random.choice(caracteres) for i in range(longueur))
    return lecode




