from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NewUser, Patient, Doctor
import uuid


class CombinedRegistrationForm(UserCreationForm):

    ROLE_CHOICES = [
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    ]

    # role dropdown
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    username = None

    # shared user fields are inside NewUser
    class Meta:
        model = NewUser
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "gender",
            "role",
        ]

    # PATIENT FIELDS
    patient_date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    patient_mobile_number = forms.CharField(required=False)
    patient_address = forms.CharField( required=False,widget=forms.TextInput(attrs={"placeholder": "Address"}))
    patient_payment_mode = forms.ChoiceField(
        required=False,
        choices=[
            ("insurance", "Insurance"),
            ("card", "Credit/Debit Card"),
            ("cash", "Cash"),
        ]
    )

    # DOCTOR FIELDS
    doctor_date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    doctor_mobile_number = forms.CharField(required=False)
    doctor_address = forms.CharField( required=False,widget=forms.TextInput(attrs={"placeholder": "Address"}))
    specialization = forms.CharField(required=False)
    license_number = forms.CharField(required=False)

    # VALIDATION LOGIC
    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")

        if role == "patient":
            required_fields = [
                "patient_date_of_birth",
                "patient_mobile_number",
                "patient_address",
                "patient_payment_mode",
            ]
        else:
            required_fields = [
                "doctor_date_of_birth",
                "doctor_mobile_number",
                "doctor_address",
                "specialization",
                "license_number",
            ]

        # Check required fields
        for field in required_fields:
            if not cleaned.get(field):
                self.add_error(field, "This field is required for selected role.")

        return cleaned

    # SAVE

    def save(self, commit=True):
        user = super().save(commit=False)

        # Auto-generate username since it's removed
        unique_part = uuid.uuid4().hex[:6]
        user.username = f"{self.cleaned_data['first_name'].lower()}{unique_part}"

        role = self.cleaned_data["role"]
        user.role = role
        user.is_active = False  # if you plan email activation later

        if commit:
            user.save()

            if role == "patient":
                Patient.objects.create(
                    user=user,
                    date_of_birth=self.cleaned_data["patient_date_of_birth"],
                    mobile_number=self.cleaned_data["patient_mobile_number"],
                    address=self.cleaned_data["patient_address"],
                    preferred_payment_mode=self.cleaned_data["patient_payment_mode"],
                )
            else:
                Doctor.objects.create(
                    user=user,
                    date_of_birth=self.cleaned_data["doctor_date_of_birth"],
                    mobile_number=self.cleaned_data["doctor_mobile_number"],
                    address=self.cleaned_data["doctor_address"],
                    specialization=self.cleaned_data["specialization"],
                    license_number=self.cleaned_data["license_number"],
                )

        return user



