from django.forms import CheckboxSelectMultiple, ModelForm
from .models import Drug_Stor, User_lab_temporary, drug_request, Register_Patient, History_patient
class DrugAdd(ModelForm):
    class Meta:
        model = Drug_Stor
        fields = '__all__'
class DrugRequestForm(ModelForm):
    class Meta:
        model = drug_request
        exclude = ['patient']
class HistoryPatientForm(ModelForm):
    class Meta:
        model = History_patient
        exclude = ['patient']

class UserLabTemporaryForm(ModelForm):
    class Meta:
        model = User_lab_temporary
        fields = ['Patient_name', 'labs']
        widgets = {
            'labs': CheckboxSelectMultiple,  # Use CheckboxSelectMultiple widget for multi-select labs
        }

        
        
    

    