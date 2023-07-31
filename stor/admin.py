from django.contrib import admin
from .models import Drug_Stor,drug_request,Register_Patient,Doctor,History_patient
from . import models
# Register your models here.
admin.site.register(Drug_Stor)
admin.site.register(drug_request)
admin.site.register(Register_Patient)
admin.site.register(Doctor)
admin.site.register(History_patient)

# admin.site.register(models.LabRequestForm)
class ListLab(admin.ModelAdmin):

    list_display = ('lab_tase_name', 'name')

admin.site.register(models.LabTestName)
admin.site.register(models.LabTest, ListLab)


admin.site.register(models.User_lab_temporary)
admin.site.register(models.LabResult)