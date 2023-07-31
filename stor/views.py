from django.shortcuts import get_object_or_404, render,redirect
from .models import Drug_Stor, LabResult, LabTestName,Register_Patient, User_lab_temporary,drug_request,Doctor, History_patient
from .forms import DrugAdd, DrugRequestForm, HistoryPatientForm, UserLabTemporaryForm
from django.template.defaultfilters import linebreaksbr
from django.apps import apps
from django.db.models import Q
# Create your views here.
def add_drug(request):
    drug_form = DrugAdd()
    if request.method == 'POST':
         drug_form = DrugAdd(request.POST)
         if drug_form.is_valid():
              drug_form.save()
              return redirect('DrugRequest')
    all_drug = Drug_Stor.objects.all()
    dictionary = {'form' : drug_form, 'all_drug' : all_drug}
    return render(request,'add_drug.html',dictionary)
def DrugRequest(request,pk):
     patient = Register_Patient.objects.get(id = pk)
     if request.method == 'POST':
        drug_request_form = DrugRequestForm(request.POST)
        if drug_request_form.is_valid():
            drug_request_obj = drug_request_form.save(commit=False)
            drug_request_obj.patient = patient
            drug_request_obj.save()
            return redirect('HistoryPatient', pk)
     else:
        drug_request_form = DrugRequestForm()
     dictionary = {'form' : drug_request_form, 'patient' : patient}
     return render(request,'drug_request.html',dictionary)
def check_drug(request, pk):
     if Drug_Stor.objects.filter(name_drug = pk).exists():
          patient_drug = Drug_Stor.objects.get(name_drug = pk)
     else:
          patient_drug = ""
     if request.method == 'POST':
         patient_id = request.session['patient_id']
         return redirect('drug_for_patient',patient_id)
     return render(request, "checkDrug.html",{'patient_drug': patient_drug})
def sell_drug(request,drug_name,pk):
	drug_request_id = drug_request.objects.get(id = pk)
	if Drug_Stor.objects.filter(name_drug = drug_request_id.drug_name).exists():
			patient_drug = Drug_Stor.objects.get(name_drug = drug_request_id.drug_name)
			patient_drug.quantity_drugs -=1
			if patient_drug.quantity_drugs == 0:
					patient_drug.delete()
			else:
				patient_drug.save()
	drug_request_id.delete()
	drug_id = request.session['patient_id']
	return redirect('drug_for_patient',drug_id)
def doctor_patients(request):
     dr_patients= Doctor.objects.all()
     dictionary = {'patients_DR' : dr_patients}
     return render(request, 'patient_for_dr.html', dictionary)
def delete_temp(request,pk):
     complit_patients = Doctor.objects.get(id = pk)
     complit_patients.delete()
     return redirect('doctor_patients')
def HistoryPatient(request,pk):
     patient = Register_Patient.objects.get(id = pk)
     print(patient.First_Name)
     print(pk,12345678)
     pre_history_patient = History_patient.objects.get(patient = patient)
     if request.method == 'POST':
        text_history = request.POST.get('text_history')
        if text_history:
             pre_history_patient.hisory_text += (f"\n\n\nName Doctor : Samuel Tolossa\n{text_history}")
             pre_history_patient.save()
     formatted_comment = linebreaksbr(pre_history_patient.hisory_text)
     dictionary = {'historyText' : formatted_comment, 'history':pre_history_patient}
     return render(request, 'history_patient.html', dictionary)
def pharma(request):
     patient_with_pharma = []
     if request.GET.get('search') != None :
        search = request.GET.get('search')
     else:
        search = '#'
    
     patients = Register_Patient.objects.filter(
        Q(full_name__icontains = search) 
        )
     patient_count = patients.count()
    
     dictionary = {'patients':patients}
     return render(request, 'pharma.html', dictionary)
def drug_for_patient(request, pk):
    request.session['patient_id'] = pk
    DrugPatient = []
    if(Register_Patient.objects.filter(id = pk).exists()):
                patient = Register_Patient.objects.get(id = pk)
                DrugPatient = drug_request.objects.filter(patient = patient)
    dictionary = {'DrugPatient':DrugPatient}
    if request.method =='POST':
         return redirect('pharma')
    return render(request, 'drug_for_patient.html', dictionary)


# def labRequest(request, pk):
#     user_id = request.GET.get('id')

    
#     user = Register_Patient.objects.get(pk=pk)
  
#     if request.method == 'POST':
#         selected_labs = request.POST.getlist('selected_labs')
#         print(selected_labs, user)
#         user_lab_temporary = User_lab_temporary.objects.create(Patient_name=user, labs=",".join(selected_labs))

#         return redirect('doctor_patients')
    
#     sections = LabTestName.objects.all()

#     return render(request, 'lab_request_form.html', {'sections': sections})

def labRequest(request, pk):
    user_id = request.GET.get('id')
    
    user = Register_Patient.objects.get(pk=pk)
   
    user = get_object_or_404(Register_Patient, pk=pk)
    print(user)
  
    if request.method == 'POST':
        selected_labs = request.POST.getlist('selected_labs')
        print(selected_labs, user)
        labs_str = ",".join(selected_labs)
        user_lab_temporary = User_lab_temporary(Patient_name=user, labs=labs_str)
        print(user_lab_temporary)
        user_lab_temporary.save()

        return redirect('doctor_patients')
    
    sections = LabTestName.objects.all()
    print(sections)

    return render(request, 'lab_request_form.html', {'sections': sections})



def save_user_lab_temporary(request):
    if request.method == 'POST':
        form = UserLabTemporaryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)  # Save the form data without committing to the database
            selected_labs = request.POST.getlist('labs')  # Get the list of selected labs from the form
            instance.save_selected_labs(selected_labs)  # Save the selected labs using the model method
            return redirect('success_url_name')  # Replace 'success_url_name' with the name of the URL pattern for the success page
    else:
        form = UserLabTemporaryForm()

    return render(request, 'lab_request_form.html', {'form': form})

def labratory(request):
    data = User_lab_temporary.objects.all()

    return render(request, 'labratory.html', {'data': data})

def labratoryToDr(request, pk):
     user = User_lab_temporary.objects.get(pk = pk)
     print(user.Patient_name)

     if request.method == "POST":
          result = request.POST.get('result')
          if result:
               res = LabResult(patient_name = user, resulut = result)
               res.save()
     
     context = {
          'user' : user
     }
     
     return render(request, 'labratory_to_doctor.html', context)


def LabratoryResult(request, pk):
     # user  = User_lab_temporary.objects.get(pk = pk)
     user = get_object_or_404(User_lab_temporary, pk=pk)
     print(user.Patient_name)
     # res = LabResult.objects.get(patient_name = user.Patient_name)
     lab_results = LabResult.objects.filter(patient_name=user.Patient_name)
     
     print(lab_results)

     context = {
          'user': user
     }

     return render(request, 'labratory_result.html', context)

