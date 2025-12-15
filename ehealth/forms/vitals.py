from django import forms
from ..models import VitalSign



class VitalSignForm(forms.ModelForm):
    class Meta:
        model = VitalSign
        fields = ["systolic_bp", "heart_rate", "temperature", "oxygen_level"]

    def save(self, commit=True):
        vital = super().save(commit=False)

        if commit:
            vital.save()
        return vital
