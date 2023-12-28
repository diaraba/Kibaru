from django.db import models
from django.contrib.auth.models import User, Group


class Personnel(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    prenom = models.CharField(max_length=255, verbose_name="Prénom")
    telephone=models.CharField(max_length=8, verbose_name="Telephone")
    adresse=models.CharField(max_length=255, verbose_name="Adresse") 
    def __str__(self):
        return f'{self.nom+ " ", +""+self.prenom}'

class Patient(models.Model):
    nom=models.CharField(max_length=255, verbose_name="Nom")
    prenom=models.CharField(max_length=255, verbose_name="Prénom")
    date_naissance=models.DateField(verbose_name="Date de naissance")
    telephone=models.CharField(max_length=8, verbose_name="Telephone")
    adresse=models.CharField(max_length=255, verbose_name="Adresse")
    statut_matrimonial=models.CharField(max_length=255, verbose_name="Statut matrimonial")
    def __str__(self):
        return f'{self.prenom+""+self.nom}'
    
class Specialite(models.Model):
    nom=models.CharField(max_length=255,verbose_name='Specialite')  
    def __str__(self) :
        return f'{self.nom}'

class Medecin(Personnel):
    age=models.PositiveIntegerField(verbose_name="age",default=0,blank=True)
    grade=models.CharField(max_length=255, verbose_name="grade")
    user = models.OneToOneField(User,related_name="medecin" ,on_delete=models.CASCADE, null=True)
    specialites=models.ManyToManyField(Specialite,related_name='medecins')
    patient=models.ManyToManyField(Patient,related_name="medecins",through="PlanifierConsultation",through_fields=('medecin', 'patient'))
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Assigner l'utilisateur au groupe des médecins
        medecin_group, created = Group.objects.get_or_create(name='Medecins')

        # Vérifier si le groupe a été créé lors de cette opération
        if created:
            # Ajouter les autorisations nécessaires au groupe ici si besoin
            pass

        # Vérifier si l'utilisateur n'appartient pas déjà au groupe
        if not self.user.groups.filter(name='Medecins').exists():
            self.user.groups.add(medecin_group)
            
        self.user.is_staff = True
        self.user.save()
    def __str__(self):
        return f'{self.prenom+""+self.nom}'




    

class AgentComptable(Personnel):
    user = models.OneToOneField(User, related_name="agent_comptable" ,on_delete=models.CASCADE, null=True)
    patient=models.ManyToManyField(Patient,related_name="agents_comptable",through="PrendreRdv")
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Assigner l'utilisateur au groupe des agents comptables
        agent_comptable_group, created = Group.objects.get_or_create(name='AgentComptables')

        # Vérifier si le groupe a été créé lors de cette opération
        if created:
            # Ajouter les autorisations nécessaires au groupe ici si besoin
            pass

        # Vérifier si l'utilisateur n'appartient pas déjà au groupe
        if not self.user.groups.filter(name='AgentComptables').exists():
            self.user.groups.add(agent_comptable_group)

        # Activer le statut staff de l'utilisateur
        self.user.is_staff = True
        self.user.save()
    def __str__(self):
        return f'{self.prenom+""+self.nom}'
        



class PlanifierConsultation(models.Model):
    date_consultation = models.DateTimeField(auto_now_add=True, verbose_name='Date consultation')
    medecin=models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True,blank=True,related_name='consultations_a_faire',verbose_name='Medecin consultant')
    patient=models.ForeignKey(Patient, on_delete=models.SET, null=True, blank=True,verbose_name='Patient',related_name='consultations_planifier')
    planificateur=models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True,blank=True,related_name='planifications',verbose_name='Planificateur')
    def __str__(self):
        return f'{self.patient}' +"  "+ f'{self.date_consultation}'

class PrendreRdv(models.Model):
    date_rdv = models.DateTimeField(auto_now_add=True, verbose_name='Date du rendez vous')
    medecin=models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True,blank=True,related_name='rdv_a_faire',verbose_name='Medecin consultant')
    patient=models.ForeignKey(Patient, on_delete=models.SET, null=True, blank=True,verbose_name='Patient',related_name='rdv')
    planificateur=models.ForeignKey(AgentComptable, on_delete=models.SET_NULL, null=True,blank=True,related_name='rdvs',verbose_name='Planificateur')
    def __str__(self):
        return f'{self.patient}' +"  "+ f'{self.date_rdv}' 

class Diagnostic(models.Model):
    motif_consultation=models.CharField(max_length=255, blank=True,verbose_name='Motif consultation')
    date_diagnostic=models.DateField(auto_now_add=True,verbose_name='Date diagnostic')
    anomalie_remarquee=models.TextField(verbose_name='Anomalie remarquée')
    medecin=models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True,blank=True,verbose_name='Medecin',related_name='diagnostics')
    patient=models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Patient',related_name='diagnostics')
    planifier_consultation=models.OneToOneField(PlanifierConsultation, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='^planifier consultation',related_name='diagnostic')
    rdv=models.OneToOneField(PrendreRdv, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Rdv',related_name='diagnostic')

class Prescription(models.Model):
    medicament_prescrit=models.TextField(verbose_name='Medicament prescrit')
    date_debut=models.DateField(verbose_name='Date de debut',auto_now_add=True, null=True, blank=True)
    date_fin=models.DateField(verbose_name='Date de fin')
    diagnostic=models.OneToOneField(Diagnostic, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Daignostic',related_name='prescription')


class Analyse(models.Model):
    description=models.TextField(verbose_name='Description')
    date=models.DateField(verbose_name='Date d\'ajout',auto_now_add=True,null=True, blank=True)
    medecin=models.ForeignKey(Medecin, on_delete=models.SET_NULL, related_name='analyses',null=True, blank=True, verbose_name='Medecin responsable')
    diagnostic=models.OneToOneField(Diagnostic, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Diagnostic',related_name='analyse')
