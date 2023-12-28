from django import forms
from .models import Patient,Diagnostic,PlanifierConsultation,PrendreRdv,Prescription,Analyse
from dal import autocomplete


class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(ConnexionForm, self).__init__(*args, **kwargs)
        # Ajoutez des classes Bootstrap aux champs du formulaire
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        # Ajoutez des classes Bootstrap aux champs du formulaire
        self.fields['nom'].widget.attrs.update({'class': 'form-control'})
        self.fields['prenom'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_naissance'].widget.attrs.update({'class': 'form-control'})
        self.fields['telephone'].widget.attrs.update({'class': 'form-control'})
        self.fields['adresse'].widget.attrs.update({'class': 'form-control'})
        self.fields['statut_matrimonial'].widget.attrs.update({'class': 'form-control'})
    

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['motif_consultation', 'anomalie_remarquee']
    def __init__(self, *args, **kwargs):
        super(DiagnosticForm, self).__init__(*args, **kwargs)
        # Ajoutez des classes Bootstrap aux champs du formulaire
        self.fields['motif_consultation'].widget.attrs.update({'class': 'form-control'})
        self.fields['anomalie_remarquee'].widget.attrs.update({'class': 'form-control'})


class PlanifierConsultationForm(forms.ModelForm):
    class Meta:
        model = PlanifierConsultation
        fields = ['medecin', 'patient']

        widgets = {
            'medecin': autocomplete.ModelSelect2(url='medecin-autocomplete'),
            'patient': autocomplete.ModelSelect2(url='patient-autocomplete')
        }
    def __init__(self, *args, **kwargs):
        super(PlanifierConsultationForm, self).__init__(*args, **kwargs)
        # Ajoutez des classes Bootstrap aux champs du formulaire
        self.fields['medecin'].widget.attrs.update({'class': 'form-control'})
        self.fields['patient'].widget.attrs.update({'class': 'form-control'})


class PrendreRdvForm(forms.ModelForm):
    class Meta:
        model = PrendreRdv
        fields = ['medecin', 'patient']

        widgets = {
            'medecin': autocomplete.ModelSelect2(url='medecin-autocomplete'),
            'patient': autocomplete.ModelSelect2(url='patient-autocomplete')
        }
    def __init__(self, *args, **kwargs):
        super(PrendreRdvForm, self).__init__(*args, **kwargs)
        # Ajoutez des classes Bootstrap aux champs du formulaire
        self.fields['medecin'].widget.attrs.update({'class': 'form-control'})
        self.fields['patient'].widget.attrs.update({'class': 'form-control'})


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicament_prescrit','date_fin']
        widgets = {
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        # Ajoutez des classes Bootstrap aux champs du formulaire
        self.fields['medicament_prescrit'].widget.attrs.update({'class': 'form-control'})

class AnalyseForm(forms.ModelForm):
    class Meta:
        model = Analyse
        fields = ['description','medecin']

        widgets = {
            'medecin': autocomplete.ModelSelect2(url='medecin-autocomplete'),
        }
    def __init__(self, *args, **kwargs):
        super(AnalyseForm, self).__init__(*args, **kwargs)
        # Ajoutez des classes Bootstrap aux champs du formulaire
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['medecin'].widget.attrs.update({'class': 'form-control'})
