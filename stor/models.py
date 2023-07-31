from django.db import models
# Create your models here.
sex = (
    ("Male","M"),
    ("Female","F"),
)

class Drug_Stor(models.Model):
    name_drug = models.CharField(max_length=100, default=None)
    quantity_drugs = models.IntegerField(default= 0)
    price_per_drug = models.IntegerField(default= 0)
    descriptions_drug = models.TextField(max_length=1000)
    def __str__(self):
            return self.name_drug
class Register_Patient(models.Model):
    """Model definition for Register_Patient."""

    First_Name = models.CharField(max_length=50)
    Middle_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, default="")
    Age = models.IntegerField(default=0)
    Sex = models.CharField(max_length=10,choices=sex)
    Address = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=15)
    Emergency_Phone_Number = models.CharField(max_length=15)
    Created_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Register_Patient."""

        verbose_name = 'Register_Patient'
        verbose_name_plural = 'Register_Patients'

    class Meta:
        ordering = ['Created_at']
        
    def __str__(self):
        """Unicode representation of Register_Patient."""
        name = self.First_Name + ' ' + self.Middle_Name + ' ' + self.Last_Name
        return name
class drug_request (models.Model):
      patient = models.ForeignKey(Register_Patient, on_delete=models.CASCADE, default=None)
      requested_at = models.DateTimeField(auto_now = True)
      drug_name = models.CharField(max_length=100)
      def __str__(self):
             return self.patient.First_Name
class History_patient(models.Model):
    patient = models.ForeignKey(Register_Patient, on_delete=models.CASCADE, default=None)
    hisory_text = models.TextField(max_length=100000000)
    def __str__(self) -> str:
          return self.patient.First_Name
class Doctor(models.Model):
     patient = models.ForeignKey(Register_Patient, on_delete=models.CASCADE, default=None)
     patient_history = models.ForeignKey(History_patient, models.CASCADE, default=None)
     First_name_Dr = models.CharField(max_length=50)
     Last_name_Dr = models.CharField(max_length=50)
     time_with_patient = models.DateTimeField(auto_now=True)
     def __str__(self):
           return self.patient.First_Name
class LabTestName(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LabTest(models.Model):
    lab_tase_name = models.ForeignKey(LabTestName, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class User_lab_temporary(models.Model):
    Patient_name = models.ForeignKey(Register_Patient, on_delete=models.PROTECT)
    # patient_name = models.CharField(max_length=100, blank=True)
    labs = models.CharField(max_length=1000, blank=True)

    # test_name = models.ForeignKey(LabTestName, on_delete=models.CASCADE)
    
    # print(labs)
    def save_selected_labs(self, selected_labs):
        labs_str = ",".join(selected_labs)
        self.labs = labs_str
        self.save()

    def get_selected_labs(self):
        return self.labs.split(",") if self.labs else []


    def __str__(self) -> str:
        return f"{self.id} {self.Patient_name} "

class LabResult(models.Model):
     patient_name = models.ForeignKey(User_lab_temporary, on_delete=models.PROTECT)

     resulut = models.CharField(max_length=1000)
     

    
      
