from django.contrib import admin
from .models import Medecin, AgentComptable,Patient,Diagnostic,PlanifierConsultation,PrendreRdv, Specialite


class MedecinAdmin(admin.ModelAdmin):
    list_display=('nom','prenom','grade')

class AgentComptableAdmin(admin.ModelAdmin): 
    list_display=('nom','prenom')

class PatientAdmin(admin.ModelAdmin):
    list_display=('nom','prenom','date_naissance')

class DiagnosticAdmin(admin.ModelAdmin):
    list_display=('motif_consultation','date_diagnostic','anomalie_remarquee')

class PlanifierConsultationAdmin(admin.ModelAdmin):
    list_display=('date_consultation','medecin','planificateur','patient')

class PrendreRdvAdmin(admin.ModelAdmin):
    list_display=('date_rdv','medecin','planificateur','patient')

class SpecialiteAdmin(admin.ModelAdmin):
    list_display=('nom',)
admin.site.register(Specialite, SpecialiteAdmin)
admin.site.register(PrendreRdv, PrendreRdvAdmin)
admin.site.register(PlanifierConsultation, PlanifierConsultationAdmin)
admin.site.register(Diagnostic, DiagnosticAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Medecin, MedecinAdmin)
admin.site.register(AgentComptable, AgentComptableAdmin)
