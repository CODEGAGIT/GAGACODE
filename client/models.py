from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from dashboard.models import Compagnie
from companyman.models import InfoLigne
from django.urls import reverse
from django.db.models.query import QuerySet

class Suggestion(models.Model):
    email=models.CharField(max_length=20)
    destinataire=models.CharField(max_length=30, default='Plateforme')
    message=models.TextField(max_length=500)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.date
    
class EtatBillet(models.Model):
        libelle=models.CharField(max_length=20)
class Billet(models.Model):
    nom_clt=models.CharField(max_length=30)
    prenom_clt=models.CharField(max_length=50)
    email_clt=models.CharField(max_length=60, blank=True, null=True)
    telephone_clt=PhoneNumberField(region='TG', # Limite le champ aux numéros américains
        blank=True, # Autorise le champ à être vide
        null=True, #Autorise le champ à être nul
        )
    code_billet=models.CharField(max_length=12)
    infoligne_id=models.ForeignKey(InfoLigne, on_delete=models.DO_NOTHING)
    prix=models.FloatField()
    place=models.SmallIntegerField()
    montant_billet=models.FloatField()
    date_heure=models.DateTimeField(auto_now_add=True)
    etat_billet=models.ForeignKey(EtatBillet, on_delete=models.DO_NOTHING, default=1)
    bl_valide=models.BooleanField(default=True)
    def __str__(self):
        return str(self.code_billet)
    
    @property
    def produit(self):
        prix_unitaire = self.prix.first() if isinstance(self.prix, QuerySet) else self.prix
        return self.place * prix_unitaire