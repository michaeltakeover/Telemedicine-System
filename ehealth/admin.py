from django.contrib import admin

# Register your models here.



from django.contrib import admin
from .models import NewUser, Patient, Doctor, ChildProfile, Appointment, VitalSign, Consultation, ChatMessage, Prescription, Notification

admin.site.register(NewUser)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(ChildProfile)
admin.site.register(Appointment)
admin.site.register(VitalSign)
admin.site.register(Consultation)
admin.site.register(ChatMessage)
admin.site.register(Prescription)
admin.site.register(Notification)

