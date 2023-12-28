from . import views
from django.urls import path, re_path
from dal import autocomplete
from hopital.models import Medecin, Patient
from hopital.views import MedecinAutocomplete, PatientAutocomplete

urlpatterns = [
    re_path(
        r'^medecin-autocomplete/$',
        MedecinAutocomplete.as_view(),
        name='medecin-autocomplete',
    ),

    re_path(
        r'^patient-autocomplete/$',
        PatientAutocomplete.as_view(),
        name='patient-autocomplete',
    ),
    path('login', views.connexion, name="login"),
    
    path('logout', views.logout_view, name="logout"),
    path('medecin_diagnostics', views.medecin_diagnostics, name='medecin_diagnostics'),
    path('ajouter_patient', views.create_patient, name='ajouter_patient'),
    path('liste_patient', views.index, name='liste_patient'),
    path('detail_patient/<int:id>', views.detail_patient, name='detail_patient'),
    path('liste_attente', views.liste_attentes, name='liste_attente'),
    path('attente_detail/<int:id>/', views.attente_detail, name='attente_detail'),
    path('attente_detail_rdv/<int:id>/', views.attente_detail_rdv, name='attente_detail_rdv'),
    path('ajouter_diagnostic/<int:id>', views.ajouter_diagnostic, name='ajouter_diagnostic'),
    path('diagnostic_detail/<int:id>/', views.diagnostic_detail, name='diagnostic_detail'),
    path('ajouter_diagnostic_rdv/<int:id>', views.ajouter_diagnostic_rdv, name='ajouter_diagnostic_rdv'),
    path('mes_diagnostic/<int:id>', views.mes_diagnostic, name='mes_diagnostic'),
    path('ajouter_planification_consultation/<int:id>', views.ajouter_planification_consultation, name='ajouter_planification_consultation'),
    path('ajouter_rdv', views.ajouter_rdv, name='ajouter_rdv'),
    path('ajouter_prescription/<int:id>', views.ajouter_prescription, name='ajouter_prescription'),
    path('ajouter_analyse/<int:id>', views.ajouter_analyse, name='ajouter_analyse'),

]