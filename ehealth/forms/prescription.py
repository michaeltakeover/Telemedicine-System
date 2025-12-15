from django import forms
from ..models import Prescription


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["medication_name", "dosage", "instructions"]
