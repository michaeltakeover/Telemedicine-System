# appointments.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Appointment, Consultation, Doctor
from ehealth.services.notification_service import send_email_notification


@login_required
def approve_appointment(request, appointment_id):
    """
     Allows an assigned doctor to approve a pending appointment.
     Ensures the user is authenticated and has a doctor role
     Verifies ownership of the appointment
     Updates appointment status to 'approved'
     Sends an email notification to the patient
    """
    if request.user.role != "doctor":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, "Profile not existing in the system.")
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
                f"Hello!\n\n"
                f"Your appointment has been approved.\n"
                f"Doctor: {doctor_name}\n"
                f"Date & Time: {appt_time}\n\n"
                f"Please log in  for more details."
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
    """
   Displays detailed appointment information for the assigned doctor.
   Patient details Appointment informationPatient vital

   """
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



@login_required
def cancel_appointment(request, appointment_id):
    """
    Cancels a pending appointment.
    The appointment status is still 'pending
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Allow only the owning patient or assigned doctor
    if request.user not in [appointment.patient.user, appointment.doctor.user]:
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    # Allow cancellation ONLY if pending
    if appointment.status != "pending":
        messages.error(
            request,
            "Only pending appointments can be cancelled."
        )
        return redirect("ehealth:home")

    # Cancel appointment
    appointment.status = "cancelled"
    appointment.save()
    messages.success(request, "Appointment cancelled.")

    if request.user.role == "doctor":
        return redirect("ehealth:doctor_dashboard")
    elif request.user.role == "patient":
        return redirect("ehealth:patient_dashboard")

    return redirect("ehealth:home")





    #  update billing
    if hasattr(appointment, "billing"):
        appointment.billing.payment_status = "cancelled"
        appointment.billing.save()


