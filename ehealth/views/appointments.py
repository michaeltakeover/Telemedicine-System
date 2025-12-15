# appointments.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Appointment, Consultation
from ..forms.appointment import AppointmentBookingForm
from ehealth.services.notification_service import send_email_notification


@login_required
def approve_appointment(request, appointment_id):
    if request.user.role != "doctor":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.doctor != request.user.doctor:
        messages.error(request, "You cannot approve this appointment.")
        return redirect("ehealth:doctor_dashboard")

    appointment.status = "approved"
    appointment.save()

    # after appointment.status = "approved" and appointment.save()

    patient_email = appointment.patient.user.email
    doctor_name = f"Dr. {appointment.doctor.user.first_name} {appointment.doctor.user.last_name}"
    appt_time = appointment.appointment_date.strftime("%d %b %Y, %H:%M")

    try:
        send_email_notification(
            to_email=patient_email,
            subject="Appointment Approved",
            message=(
                f"Good news!\n\n"
                f"Your appointment has been approved.\n"
                f"Doctor: {doctor_name}\n"
                f"Date & Time: {appt_time}\n\n"
                f"Please log in to your dashboard for more details."
            )
        )
    except Exception as e:
        print("Patient notification failed:", e)

    Consultation.objects.get_or_create(
        appointment=appointment,
        defaults={"consultation_type": "chat"}
    )

    messages.success(request, "Appointment approved.")
    return redirect("ehealth:doctor_dashboard")




@login_required
def doctor_appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user.role != "doctor":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    if appointment.doctor != request.user.doctor:
        messages.error(request, "Access denied.")
        return redirect("ehealth:doctor_dashboard")

    patient = appointment.patient
    vitals = patient.vitals.order_by("-created_at")

    context = {
        "appointment": appointment,
        "patient": patient,
        "vitals": vitals,
    }

    return render(
        request,
        "ehealth/doctor_appointment_detail.html",
        context
    )

