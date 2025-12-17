from django import forms
from django.utils.timezone import now
from ..models import Appointment, Doctor, ChildProfile




class AppointmentBookingForm(forms.ModelForm):

    child = forms.ModelChoiceField(
        queryset=ChildProfile.objects.none(),
        required=False,
        empty_label="In"
    )

    class Meta:
        model = Appointment
        fields = ["doctor", "child", "appointment_date", "reason"]
        widgets = {
            "appointment_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "min": now().strftime("%Y-%m-%dT%H:%M")
                }
            )
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop("patient")
        super().__init__(*args, **kwargs)

        children = ChildProfile.objects.filter(parent=patient)
        if children.exists():
            self.fields["child"].queryset = children
        else:
            self.fields.pop("child")

        self.fields["doctor"].queryset = Doctor.objects.filter(is_approved=True)

