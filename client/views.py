from django.shortcuts import render,HttpResponse,get_list_or_404,get_object_or_404,redirect,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from . import forms,models
import datetime
from dashboard.models import Compagnie,Ville
from companyman.models import Ligne,InfoLigne,Bus
from .functions import code
from django.db.models.query import QuerySet
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import black
from reportlab.platypus import Paragraph, Spacer, Image
from django.template.loader import get_template
from django.template import Context



lecode=code(8)
ville= Ville.objects.all()
ligne= Ligne.objects.all()
infln= InfoLigne.objects.all()
comp= Compagnie.objects.all()
bus= Bus.objects.all()
dnow= datetime.date.today()
dateheure=datetime.datetime.now()
etat=models.EtatBillet.objects.all()
lesdates=InfoLigne.objects.filter(date_dep__gt=datetime.datetime.now()).values_list('date_dep')

def accueil_view(request):
    context = {
        "ville":ville,
        "ligne": ligne,
        "infln": infln,
        "comp": comp,
        "lesbus": bus,
        "dnow": dnow,
    }
    return render(request,'index.html',context)
    
def suggestionForm(request):
    form=forms.SuggestionForm(request.POST)
    if form.is_valid():
        form.save()
        form=forms.SuggestionForm() 
    context={'form':form,}
    return render(request,'suggestion.html',context)

def reservation1_view(request):
    context={'rdt':lesdates,}
    return render(request,'reservation_etape1.html',context)


def listechoix_view(request):
    
    context={'rdt':lesdates,
             'infln':infln,
             'lignes':ligne,}
    return render(request,'listechoix.html',context)


def infoligne_view(request,ln_id):
    context={'ln':get_object_or_404(Ligne, pk=ln_id),
             'infln':infln.filter(ligne_id=ln_id),
             }
    return render(request,'infoligne.html',context)

def update_places_disponibles(infoligne_id, nb_places_res):
    """
    Fonction pour mettre à jour le nombre de places disponibles dans le modèle Infoligne.
    """
    infoligne = InfoLigne.objects.get(pk=infoligne_id)
    infoligne.place_restante -= nb_places_res
    infoligne.save()


def reservation2_view(request, res_id):
    res = get_object_or_404(InfoLigne, pk=res_id)
    if request.method == 'POST':
        formulaire = forms.BilletForm(request.POST)
        context = {
            'res': res,
            'inf': infln.get(pk=res_id),
            'form1': formulaire,
            'lecode': lecode,
            'prix': InfoLigne.objects.filter(id=res_id).values_list('prix', flat=True),
        }
        if formulaire.is_valid():
            donnees = formulaire.cleaned_data
            if donnees['place'] <= res.place_restante:
                montant = models.Billet(place=donnees['place'], prix=context['prix'])
                billet = forms.Billet.objects.create(
                    nom_clt=donnees['nom_clt'],
                    prenom_clt=donnees['prenom_clt'],
                    email_clt=donnees['email_clt'],
                    telephone_clt=donnees['telephone_clt'],
                    place=donnees['place'],
                    code_billet=lecode, # une fonction qui génère un code unique pour chaque billet
                    infoligne_id=context['inf'],
                    prix=context['prix'],
                    montant_billet=montant.produit,
                    bl_valide=True,
                )
                billet.save()
                update_places_disponibles(context['inf'].pk, donnees['place'])
                return redirect(reverse('client:billet_detail_view', args=[billet.pk]))
            else:
                max_place = res.place_restante
                message = f"Le nombre de places que vous pouvez choisir est maximum {max_place}"
                context['message'] = message
        else:
            context['form1'] = formulaire
    else:
        formulaire = forms.BilletForm()
        context = {
            'res': get_object_or_404(InfoLigne, pk=res_id),
            'inf': infln.get(pk=res_id),
            'form1': formulaire,
        }
    return render(request, 'reservation_etape2.html', context)

def billet_detail_view(request, billet_id):
    billet = get_object_or_404(models.Billet, pk=billet_id)
    infoln = get_object_or_404(InfoLigne, pk=billet.infoligne_id.pk)
    context = {
        'billet': billet,
        'infoln' : infoln,
        'ligne' : ligne,
        }
    return render(request, 'billet_detail.html', context)


def generate_pdf(request, billet_id):
    # Get the Billet object with the specified ID
    billet = models.Billet.objects.get(id=billet_id)

    # Create a new PDF object using ReportLab Canvas
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Billet_{}-{}.pdf"'.format(
        billet.nom_clt.replace(" ", "_"), billet.id
    )
    pdf_canvas = canvas.Canvas(response)

    # Add content to the PDF
    pdf_canvas.drawString(80, 800, "{}".format(billet.date_heure))
    pdf_canvas.drawString(130, 750, "VOTRE BILLET : ")
    pdf_canvas.drawString(100, 700, "Ligne: {} - {} ".format(billet.infoligne_id.ligne_id.ville_dep.nom_ville , billet.infoligne_id.ligne_id.ville_arr.nom_ville))
    pdf_canvas.drawString(100, 650, "Nom: {}".format(billet.nom_clt))
    pdf_canvas.drawString(100, 600, "Prénom: {}".format(billet.prenom_clt))
    pdf_canvas.drawString(100, 550, "Téléphone: {}".format(billet.telephone_clt))
    pdf_canvas.drawString(100, 500, "Email: {}".format(billet.email_clt))
    pdf_canvas.drawString(100, 450, "Code du billet: {}".format(billet.code_billet))
    pdf_canvas.drawString(100, 400, "Prix unitaire: {}".format(billet.prix))
    pdf_canvas.drawString(100, 350, "Nombre de places: {}".format(billet.place))
    pdf_canvas.drawString(100, 300, "Montant total: {}".format(billet.montant_billet))
    pdf_canvas.drawString(100, 250, "Date et heure de départ: {}".format(billet.infoligne_id.date_dep))


    # Finish the PDF
    pdf_canvas.showPage()
    pdf_canvas.save()

    return response


def recherche1_view(request):
    if request.method == 'POST':
        recherche = forms.RechercheBillet(request.POST)
        if recherche.is_valid():
            donnees = recherche.cleaned_data
            code = donnees['code_billet']
            resultat = models.Billet.objects.filter(code_billet=code).first()
            if resultat is not None:
                id_billet = resultat.id
                return redirect(reverse('client:annulation2', args=[id_billet]))
            else:
                message = "Aucun billet ne correspond à ce code"
                return HttpResponse(message)
    else:
        recherche = forms.RechercheBillet()
    context = {
        'recherche': recherche,
    }
    return render(request, 'annulation1.html', context)

def annulation_view(request, billet_id):
    billet = get_object_or_404(models.Billet, id=billet_id)
    infoln = get_object_or_404(models.InfoLigne, id=billet.infoligne_id.id)
    etatb=get_object_or_404(models.EtatBillet, id=billet.etat_billet.id)
    context = {
        'billet': billet,
        'infoln': infoln,
        'ligne': ligne,
        'etat':etatb,
    }
    
    return render(request, 'annulation2.html', context)

def annuler_billet(request, billet_id):
    billet = get_object_or_404(models.Billet, id=billet_id)
    billet.etat_billet = models.EtatBillet.objects.get(id=3)
    billet.bl_valide = False
    billet.save()

    return redirect('client:billet_detail_view', billet_id=billet.id)


def recherche2_view(request):
    if request.method == 'POST':
        recherche = forms.RechercheBillet(request.POST)
        if recherche.is_valid():
            donnees = recherche.cleaned_data
            code = donnees['code_billet']
            resultat = models.Billet.objects.filter(code_billet=code).first()
            if resultat is not None:
                id_billet = resultat.id
                return redirect(reverse('client:modification2', args=[id_billet]))
            else:
                message = "Aucun billet ne correspond à ce code"
                return HttpResponse(message)
    else:
        recherche = forms.RechercheBillet()
    context = {
        'recherche': recherche,
    }
    return render(request, 'modification1.html', context)

def modifier_billet(request, billet_id):
    billet = get_object_or_404(models.Billet, id=billet_id)

    if request.method == 'POST':
        form = forms.BilletForm(request.POST, instance=billet)
        if form.is_valid():
            form.save()
            return redirect('client:billet_detail_view', billet_id=billet.id)
    else:
        form = forms.BilletForm()

    context = {
        'form': form,
        'billet': billet
    }
    return render(request, 'modification2.html', context)

def lescompagnies_view(request):
    context={
        'comp':comp,
             }
    return render(request,'lescompagnies.html',context)

def lacompagnie_view(request,cp_id):
    infos = InfoLigne.objects.filter(bus_id__compagnie_id=cp_id)
    context={
        'cp':get_object_or_404(Compagnie, pk=cp_id),
        'infos': infos,
    }
    return render(request,'lacompagnie.html',context)
