"""
PrescriptionForm

form is used by a doctor to create or update a prescription
during or after a consultation such as the drug name, dosage, and usage instructions.

"""

from django import forms
from ..models import Prescription


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["medication_name", "dosage", "instructions"]
