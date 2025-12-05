from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class BaseUserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ["phone", "gender", "birthdate"]


class PatientRegistrationForm(BaseUserForm):
    """Form for patients only."""

    def save(self, commit=True):
        # Create User model object
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"]
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        # Create Profile
        profile = UserProfile(
            user=user,
            role="patient",
            phone=self.cleaned_data["phone"],
            gender=self.cleaned_data["gender"],
            birthdate=self.cleaned_data["birthdate"],
            specialty=None,
            license_number=None,
            verification_status=None
        )

        if commit:
            profile.save()

        return profile


class DoctorRegistrationForm(BaseUserForm):
    """Form for doctors only."""

    specialty = forms.CharField()
    license_number = forms.CharField()

    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields + ["specialty", "license_number"]

    def save(self, commit=True):
        # Create User model
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"]
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        # Create UserProfile model
        profile = UserProfile(
            user=user,
            role="doctor",
            phone=self.cleaned_data["phone"],
            gender=self.cleaned_data["gender"],
            birthdate=self.cleaned_data["birthdate"],
            specialty=self.cleaned_data["specialty"],
            license_number=self.cleaned_data["license_number"],
            verification_status=False
        )

        if commit:
            profile.save()

        return profile
