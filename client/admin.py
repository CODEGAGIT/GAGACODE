from django.contrib import admin
from .models import Suggestion,Billet,EtatBillet

admin.site.register(Suggestion)
admin.site.register(Billet)
admin.site.register(EtatBillet)