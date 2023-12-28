from django.shortcuts import  get_object_or_404, render, redirect
from .models import AgentComptable, Patient, Medecin,PlanifierConsultation,Diagnostic, PrendreRdv,Prescription,Analyse
from django.contrib.auth.decorators import user_passes_test
from .forms import PatientForm, DiagnosticForm, PlanifierConsultationForm,PrendreRdvForm,PrescriptionForm,AnalyseForm,ConnexionForm
from django.contrib import messages
from dal import autocomplete
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from .exception import get_diagnostic_by_planifier_consultation_id,  get_diagnostic_by_rdv_id,  get_analyse_by_diagnostic_id,  get_prescription_by_diagnostic_id,  get_medecin_by_user_id


def is_medecin(user):
    if user.groups.filter(name='Medecins').exists():
        return True

def is_agent_comptable(user):
    return user.groups.filter(name='AgentComptables').exists()



@user_passes_test(is_medecin)
def medecin_diagnostics(request):
    medecin = get_medecin_by_user_id(request.user.id)
    diagnostics = medecin.diagnostics.all()
    medecin1=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    params = {
        'diagnostics': diagnostics,
        'medecin': medecin1,
        'agent_comptable': agent_comptable
        }
    return render(request, 'hopital/medecin/medecin_diagnostics.html', params)


def connexion(request):
   if request.method == 'POST':
       form = ConnexionForm(request.POST)
       if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username, password=password)
           if user is not None:
               login(request, user)
               messages.add_message(request, messages.SUCCESS, "")
               return redirect('liste_patient')
           else:
                messages.set_level(request, messages.ERROR)
                messages.add_message(request, messages.ERROR, "Login ou mot de pass incorrect")
       else:
            messages.set_level(request, messages.ERROR)
            messages.add_message(request, messages.ERROR, "Login et mot de passe obligatoire")
   else:
        form = ConnexionForm()
   return render(request, 'hopital/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def create_patient(request):
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)    
    if (request.method == 'POST'):
        obj=Patient()
        patient=PatientForm(request.POST, instance=obj)
        patient.save() 
        return redirect('liste_patient')
    else:
        params = {
            'form': PatientForm(),
            'medecin': medecin,
            'agent_comptable': agent_comptable
        }
        return render(request, 'hopital/patient/create_patient.html', params)


def index(request):
    patients = Patient.objects.all()
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    params = {
        'patients': patients,
        'medecin': medecin,
        'agent_comptable': agent_comptable
        }
    return render(request, 'hopital/patient/index.html', params)


def detail_patient(request, id):
    patient = Patient.objects.get(id=id)
    consultations_planifier=patient.consultations_planifier.all()
    rdvs=patient.rdv.all()
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    params = {
        'patient': patient,
        'consultations':consultations_planifier,
        'rdvs':rdvs,
        'medecin': medecin,
        'agent_comptable': agent_comptable
        }
    return render(request, 'hopital/patient/detail.html', params)

def liste_attentes(request):
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    if not request.user.is_authenticated:
        return render(request, 'hopital/404.html')
    
    try:
        medecin=request.user.medecin
    except Medecin.DoesNotExist:
        return render(request, 'hopital/404.html')
    
    consultations_planifier=medecin.consultations_a_faire.all()
    rdv=medecin.rdv_a_faire.all()
    params = {
        'consultations':consultations_planifier,
        'rdvs':rdv,
        'medecin': medecin,
        'agent_comptable': agent_comptable
        }
    return render(request, 'hopital/medecin/liste_attente.html', params)

def attente_detail(request, id):
    consultations_planifier = PlanifierConsultation.objects.get(id=id)
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    params = {
        'consultation':consultations_planifier,
        'medecin': medecin,
        'agent_comptable': agent_comptable
        }
    return render(request, 'hopital/medecin/attente_detail.html', params)

def attente_detail_rdv(request, id):
    rdv = PrendreRdv.objects.get(id=id),
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    params = {
        'rdv':rdv,
        'medecin': medecin,
        'agent_comptable': agent_comptable
        }
    return render(request, 'hopital/medecin/attente_detail_rdv.html', params)


def ajouter_diagnostic(request, id):
    planifier_consultation = PlanifierConsultation.objects.get(id=id)
    medecin=planifier_consultation.medecin
    diagnostic1 = get_diagnostic_by_planifier_consultation_id(id)
    medecin1=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)

    if not request.user.is_authenticated:
        return render(request, 'hopital/404.html')
    if diagnostic1 is not None:
        messages.error(request, 'Un diagnostic existe déja ')
        return redirect('attente_detail' ,id=id)
    try:
        if request.user.is_authenticated and request.user.medecin.id==medecin.id:
            if (request.method == 'POST'):
                obj=Diagnostic()
                diagnostic_form=DiagnosticForm(request.POST, instance=obj)
                if diagnostic_form.is_valid():
                    diagnostic = diagnostic_form.save(commit=False)
                    diagnostic.medecin=medecin
                    diagnostic.patient=planifier_consultation.patient
                    diagnostic.planifier_consultation=planifier_consultation 
                    diagnostic.save() 
                    messages.add_message(request, messages.SUCCESS,'Le diagnostic a été ajouté avec succès')
                    return redirect('attente_detail', id=id)
                else:
                    # Si le formulaire n'est pas valide, affichez un message d'erreur
                    messages.error(request, 'Le formulaire de diagnostic n\'est pas valide. Veuillez corriger les erreurs')

            else:
                params = {
                    'form': DiagnosticForm(),
                    'planifier_consultation':planifier_consultation,
                    'medecin': medecin1,
                    'agent_comptable': agent_comptable
                }
                return render(request, 'hopital/medecin/ajouter_diagnostic.html', params)
        else:
            return render(request, 'hopital/404.html')
    except Medecin.DoesNotExist:
        return render(request, 'hopital/404.html')
    


def ajouter_diagnostic_rdv(request, id):
    rdv = PrendreRdv.objects.get(id=id)
    medecin=rdv.medecin
    diagnostic1 =get_diagnostic_by_rdv_id(id)
    medecin1=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)

    if not request.user.is_authenticated:
        return render(request, 'hopital/404.html')
    if diagnostic1 is not None:
        messages.error(request, 'Un diagnostic existe déja  ')
        return redirect('attente_detail_rdv' ,id=id)    
    try:
        if request.user.is_authenticated and request.user.medecin.id==medecin.id:
            if (request.method == 'POST'):
                obj=Diagnostic()
                diagnostic_form=DiagnosticForm(request.POST, instance=obj)
                if diagnostic_form.is_valid():
                    diagnostic = diagnostic_form.save(commit=False)
                    diagnostic.medecin=medecin
                    diagnostic.patient=rdv.patient
                    diagnostic.rdv=rdv 
                    diagnostic.save() 
                    messages.add_message(request, messages.SUCCESS,'Le diagnostic a été ajouté avec succès')
                    return redirect('diagnostic_detail', id=diagnostic.id)
                else:
                    # Si le formulaire n'est pas valide, affichez un message d'erreur
                    messages.error(request, 'Le formulaire de diagnostic n\'est pas valide. Veuillez corriger les erreurs')

            else:
                params = {
                    'form': DiagnosticForm(),
                    'rdv':rdv,
                    'medecin': medecin1,
                    'agent_comptable': agent_comptable
                }
                return render(request, 'hopital/medecin/ajouter_diagnostic_rdv.html', params)
        else:
            return render(request, 'hopital/404.html')
    except Medecin.DoesNotExist:
        return render(request, 'hopital/404.html')



def mes_diagnostic(request,id):
    patient = Patient.objects.get(id=id)
    diagnostics=patient.diagnostics.all()
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    params = {
        'patient': patient,
        'diagnostics':diagnostics,
        'medecin': medecin,
        'agent_comptable': agent_comptable
    }
    return render(request, 'hopital/patient/mes_diagnostics.html', params)




def ajouter_planification_consultation(request, id):
    patient=Patient.objects.get(id=id)
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    if not request.user.is_authenticated:
        return render(request, 'hopital/404.html')
    try:
        if request.user.is_authenticated:
            if (request.method == 'POST'):
                obj=PlanifierConsultation()
                planification_form=PlanifierConsultationForm(request.POST, instance=obj)
                if planification_form.is_valid():
                    planification = planification_form.save(commit=False)
                    planification.planificateur=request.user.medecin
                    planification.save() 
                    messages.add_message(request, messages.SUCCESS,'La planification de la consultation a été ajouté avec succès')
                    return redirect('liste_patient')
                else:
                    # Si le formulaire n'est pas valide, affichez un message d'erreur
                    messages.error(request, 'Le formulaire de planification de la consultation n\'est pas valide. Veuillez corriger les erreurs')
            else:
                params={
                    'form': PlanifierConsultationForm(),
                    'patient':patient,
                    'medecin': medecin,
                    'agent_comptable': agent_comptable
                }
                return render(request, 'hopital/medecin/ajouter_planification_consultation.html',params)
        else:
                    return render(request, 'hopital/404.html')
    except Medecin.DoesNotExist:
        return render(request, 'hopital/404.html')




def ajouter_rdv(request):
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    if not request.user.is_authenticated:
        return render(request, 'hopital/404.html')
    try:
        if request.user.is_authenticated:
            if (request.method == 'POST'):
                obj=  PrendreRdv()
                rdv_form=PrendreRdvForm(request.POST, instance=obj)
                if rdv_form.is_valid():
                    rdv = rdv_form.save(commit=False)
                    rdv.planificateur=request.user.agent_comptable
                    rdv.save() 
                    messages.add_message(request, messages.SUCCESS,'Le rendez vous pour la consultation a été ajouté avec succès')
                    return redirect('liste_patient')
                else:
                    # Si le formulaire n'est pas valide, affichez un message d'erreur
                    messages.error(request, 'Le formulaire de prise de rendez vous pour la consultation n\'est pas valide. Veuillez corriger les erreurs')
            else:
                params={
                    'form': PlanifierConsultationForm(),
                    'medecin': medecin,
                    'agent_comptable': agent_comptable
                }
                return render(request, 'hopital/medecin/ajouter_rdv.html',params)
        else:
                    return render(request, 'hopital/404.html')
    except AgentComptable.DoesNotExist:
        return render(request, 'hopital/404.html')



#l'ajout de l'autocompletion du medecin c'est une classe importante pour implementer l'auto completion
class MedecinAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Medecin.objects.none()

        qs = Medecin.objects.all()

        if self.q:
                qs = qs.filter(Q(prenom__istartswith=self.q) | Q(nom__istartswith=self.q))

        return qs

# PatientAutocomplete est une classe importante pour implementer l'auto completion
class PatientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Nous permet de nous assurer que ca ne marche que si on est authetifié!
        if not self.request.user.is_authenticated:
            return Patient.objects.none()

        qs = Patient.objects.all()

        if self.q:
                qs = qs.filter(Q(prenom__istartswith=self.q) | Q(nom__istartswith=self.q))
        return qs



def diagnostic_detail(request, id):
    diagnostic = Diagnostic.objects.get(id=id)
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    params = {
        'diagnostic':diagnostic,
        'medecin': medecin,
        'agent_comptable': agent_comptable
        }
    return render(request, 'hopital/medecin/diagnostic_detail.html', params)




def ajouter_prescription(request, id):
    diagnostic=Diagnostic.objects.get(id=id)
    prescription = get_prescription_by_diagnostic_id(id)
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    if not request.user.is_authenticated:
        return render(request, 'hopital/404.html')
    if prescription is not None:
        messages.error(request, 'Une prescription existe déja pour ce diagnostic')
        return redirect('diagnostic_detail' ,id=id)    
    try:
        if request.user.is_authenticated and request.user.medecin.id==diagnostic.medecin.id:
            if (request.method == 'POST'):
                obj=  Prescription()
                prescription_form=PrescriptionForm(request.POST, instance=obj)
                if prescription_form.is_valid():
                    prescription = prescription_form.save(commit=False)
                    prescription.diagnostic=diagnostic
                    prescription.save() 
                    messages.add_message(request, messages.SUCCESS,'La prescription a été ajouté avec succès')
                    return redirect('diagnostic_detail' ,id=id)
                else:
                    # Si le formulaire n'est pas valide, affichez un message d'erreur
                    messages.error(request, 'Le formulaire d\'ajout de la prescription n\'est pas valide. Veuillez corriger les erreurs')
            else:
                params={
                    'form': PrescriptionForm(),
                    'diagnostic':diagnostic,
                    'medecin': medecin,
                    'agent_comptable': agent_comptable
                }
                return render(request, 'hopital/medecin/ajouter_prescription.html',params)
        else:
                    return render(request, 'hopital/404.html')
    except Medecin.DoesNotExist:
        return render(request, 'hopital/404.html')
    



def ajouter_analyse(request, id):
    diagnostic=Diagnostic.objects.get(id=id)
    analyse = get_analyse_by_diagnostic_id(id) 
    medecin=is_medecin(request.user)
    agent_comptable=is_agent_comptable(request.user)
    if not request.user.is_authenticated:
        return render(request, 'hopital/404.html')
    if analyse is not None:
        messages.error(request, 'Une analyse existe déja pour ce diagnostic')
        return redirect('diagnostic_detail' ,id=id)
    try:
        if request.user.is_authenticated and request.user.medecin.id==diagnostic.medecin.id:
            if (request.method == 'POST'):
                obj=  Analyse()
                analyse_form=AnalyseForm(request.POST, instance=obj)
                if analyse_form.is_valid():
                    analyse = analyse_form.save(commit=False)
                    analyse.diagnostic=diagnostic
                    analyse.save() 
                    messages.add_message(request, messages.SUCCESS,'L\'analyse  a été ajouté avec succès')
                    return redirect('diagnostic_detail' ,id=id)
                else:
                    # Si le formulaire n'est pas valide, affichez un message d'erreur
                    messages.error(request, 'Le formulaire d\'ajout de l\'analyse  n\'est pas valide. Veuillez corriger les erreurs')
            else:
                params={
                    'form': AnalyseForm(),
                    'diagnostic':diagnostic,
                    'medecin': medecin,
                    'agent_comptable': agent_comptable                    
                }
                return render(request, 'hopital/medecin/ajouter_analyse.html',params)
        else:
                    return render(request, 'hopital/404.html')
    except Medecin.DoesNotExist:
        return render(request, 'hopital/404.html')