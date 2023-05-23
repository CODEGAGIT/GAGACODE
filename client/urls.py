from django.urls import path
from . import views

app_name="client"

urlpatterns = [
    path('',views.accueil_view,name='accueil'),
    path('suggestion/',views.suggestionForm,name='suggestion'),
    path('etape1/',views.reservation1_view,name='etape1'),
    path('listechoix/',views.listechoix_view,name='listechoix'),
    path('etape2/details/<int:billet_id>/',views.billet_detail_view,name='billet_detail_view'),
    path('etape2/<int:res_id>/',views.reservation2_view,name='etape2'),
    path('infoligne/<int:ln_id>/',views.infoligne_view, name='infoligne'),
    path('annulation1/',views.recherche1_view,name='annulation1'),
    path('annulation2/<int:billet_id>/',views.annulation_view,name='annulation2'),
    path('annulation3/<int:billet_id>/',views.annuler_billet,name='annulation3'),
    path('modification1/',views.recherche2_view,name='modification1'),
    path('modification2/<int:billet_id>/',views.modifier_billet,name='modification2'),
    path('compagnies/',views.lescompagnies_view,name='lescompagnies'),
    path('compagnie/<int:cp_id>/',views.lacompagnie_view, name='lacompagnie'),
    path('generate-pdf/<int:billet_id>/', views.generate_pdf, name='generate_pdf'),
]

