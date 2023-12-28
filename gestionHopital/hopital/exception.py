from .models import Analyse, Medecin, PlanifierConsultation,PrendreRdv, Diagnostic, Prescription
from django.contrib.auth.models import User

#ces fonctions me permet de recuperer des objets tout en gerant l'exeption DoesNotExit
def get_diagnostic_by_planifier_consultation_id(planifier_consultation_id):
    try:
        planifier_consultation = PlanifierConsultation.objects.get(id=planifier_consultation_id)

        diagnostic = Diagnostic.objects.get(planifier_consultation=planifier_consultation)

        return diagnostic
    except Diagnostic.DoesNotExist:
        # Gérer le cas où l'instance de Diagnostic n'existe pas
        return None

def get_diagnostic_by_rdv_id(rdv_id):
    try:
        rdv = PrendreRdv.objects.get(id=rdv_id)

        diagnostic = Diagnostic.objects.get(rdv=rdv)

        return diagnostic
    except Diagnostic.DoesNotExist:
        # Gérer le cas où l'instance de Diagnostic n'existe pas
        return None

def get_analyse_by_diagnostic_id(diagnostic_id):
    try:
        diagnostic = Diagnostic.objects.get(id=diagnostic_id)

        analyse = Analyse.objects.get(diagnostic=diagnostic)

        return analyse
    except Analyse.DoesNotExist:
        # Gérer le cas où l'instance de Analyse n'existe pas
        return None


def get_prescription_by_diagnostic_id(diagnostic_id):
    try:
        diagnostic = Diagnostic.objects.get(id=diagnostic_id)

        prescription = Prescription.objects.get(diagnostic=diagnostic)

        return prescription
    except Prescription.DoesNotExist:
        # Gérer le cas où l'instance de Prescription n'existe pas
        return None

def get_medecin_by_user_id(user_id):
    try:
        user = User.objects.get(id=user_id)

        medecin = Medecin.objects.get(user=user)

        return medecin
    except Medecin.DoesNotExist:
        # Gérer le cas où l'instance de Medecin n'existe pas
        return None