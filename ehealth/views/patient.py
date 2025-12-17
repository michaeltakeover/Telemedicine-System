"""
Patient-related views for the Telemedicine System.
patient  appointment booking,vital sign updates, and notification workflows. Access is restricted
to authenticated users with the patient role.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from ..models import Patient, Appointment
from ..forms import AppointmentBookingForm, VitalSignForm
from ehealth.services.notification_service import send_email_notification



@login_required
def patient_dashboard(request):
    """
    Displays the patient dashboard.
    Shows the patient's profile information, appointment history,
    """
    if request.user.role != "patient":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(
            request,
            "Your patient profile is incomplete. Please contact support."
        )
        return redirect("ehealth:home")

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-appointment_date")

    context = {
        "patient": patient,
        "appointments": appointments,
        "vitals": patient.vitals.order_by("-created_at")[:5],
    }

    return render(request, "ehealth/patient_dashboard.html", context)



@login_required
def book_appointment(request):
    """
    appointment booking for patients,Allows a patient to request an appointment with an approved doctor.
    The appointment when  created is in  a 'pending' status and a notification is sent to the selected doctor.
    """
    if request.user.role != "patient":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    patient = request.user.patient

    if request.method == "POST":
        form = AppointmentBookingForm(request.POST, patient=patient)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.status = "pending"

            #
            child = form.cleaned_data.get("child")
            if child and child.parent != patient:
                messages.error(request, "Invalid child selection.")
                return redirect("ehealth:home")

            appointment.save()

            doctor_email = appointment.doctor.user.email
            patient_name = f"{appointment.patient.user.first_name} {appointment.patient.user.last_name}"
            appt_time = appointment.appointment_date.strftime("%d %b %Y, %H:%M")

            try:
                send_email_notification(
                    to_email=doctor_email,
                    subject="New Appointment Request",
                    message=(
                        f"You have a new appointment request.\n\n"
                        f"Patient: {patient_name}\n"
                        f"Date & Time: {appt_time}\n"
                        f"Status: Pending approval."
                    )
                )
            except Exception as e:
                print("Email notification failed:", e)


            messages.success(request, "Appointment booked successfully.")
            return redirect("ehealth:patient_dashboard")

    else:
        form = AppointmentBookingForm(patient=patient)

    return render(
        request,
        "ehealth/book_appointment.html",
        {"form": form}
    )


@login_required
def add_vitals(request):
    """
    Records patient vital signs.
    """
    if request.user.role != "patient":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    patient = request.user.patient

    last_vital = patient.vitals.order_by("-created_at").first()

    if last_vital:
        time_diff = timezone.now() - last_vital.created_at

        if time_diff < timedelta(hours=1):
            remainining_time = 60 - int(time_diff.total_seconds()/60)
            messages.error(request, f"You can record the vitals again after {remainining_time} seconds.")
            return redirect("ehealth:view_vitals")

    if request.method == "POST":
        form = VitalSignForm(request.POST)
        if form.is_valid():
            vital = form.save(commit=False)
            vital.patient = patient
            vital.save()

            alerts = vital.out_of_range_vitals()

            if alerts:
                send_email_notification(
                    to_email=settings.ADMIN_EMAIL,
                    subject="Abnormal Patient Vitals Alert",
                    message=(
                            f"Patient: {vital.patient.user.first_name} "
                            f"{vital.patient.user.last_name}\n\n"
                            f"Abnormal readings detected:\n"
                            + "\n".join(alerts)
                    )
                )
        messages.success(request, "Vitals recorded successfully.")
        return redirect("ehealth:patient_dashboard")
    else:
        form = VitalSignForm()

    return render(
        request,
        "ehealth/add_vitals.html",
        {"form": form}
    )

