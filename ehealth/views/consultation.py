# consultation.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Appointment, Consultation, ChatMessage, Patient,Doctor,Prescription,VitalSign
from ..forms import PrescriptionForm


@login_required
def view_vitals(request, patient_id=None):
    """
    Shared vitals view for patient and doctor
    """

    # Patient viewing own vitals
    if request.user.role == "patient":
        patient = request.user.patient

    #  Doctor viewing a patient's vitals
    elif request.user.role == "doctor":
        patient = get_object_or_404(Patient, id=patient_id)

    else:
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    vitals = patient.vitals.order_by("-created_at")

    return render(request,"ehealth/vitals_table.html",
        {
            "patient": patient,
            "vitals": vitals
        }
    )

@login_required
def consultation_chat(request, appointment_id):
    """
    Manages the consultation chat between a doctor and a patient.
    Once an appointment is marked as completed, the chat becomes
    read-only to preserve consultation integrity.
    """

    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Allow BOTH doctor and patient
    if request.user not in [
        appointment.doctor.user,
        appointment.patient.user
    ]:
        return HttpResponseForbidden("Access denied")

    consultation, _ = Consultation.objects.get_or_create(
        appointment=appointment,
        defaults={"consultation_type": "chat"}
    )

    messages_qs = ChatMessage.objects.filter(
        consultation=consultation
    ).order_by("timestamp")

    is_read_only = appointment.status == "completed"

    if request.method == "POST" and not is_read_only:
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(
                consultation=consultation,
                sender=request.user,
                message=message_text
            )

    return render(
        request,
        "ehealth/consultation_chat.html",
        {
            "appointment": appointment,
            "consultation": consultation,
            "messages": messages_qs,
            "is_read_only": is_read_only,
        }
    )

@login_required
def create_prescription(request, appointment_id):
    """
    Allows a doctor to create a prescription for a completed appointment.
    Appointments with a status of 'completed'
    Prescriptions are linked to both the consultation and the prescribing doctor.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if (
            request.user.role != "doctor"
            or appointment.doctor is None
            or request.user.id != appointment.doctor.user.id
            or appointment.status != "completed"
    ):
            return HttpResponseForbidden("Access denied")

    consultation = appointment.consultation



    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.consultation = consultation
            prescription.doctor = appointment.doctor
            prescription.save()

            #return redirect("ehealth:doctor_dashboard")
            return redirect(
                "ehealth:view_prescriptions",
                appointment_id=appointment.id)


    else:
        form = PrescriptionForm()

    return render(request, "ehealth/create_prescription.html", {
        "appointment": appointment,
        "form": form,
    })

@login_required
def save_notes(request, appointment_id):
    """
    Saves clinical notes entered by the assigned doctor
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Security: only the assigned doctor can save notes
    if (request.user != appointment.doctor.user
        or appointment.status != "completed"):
        messages.error(request, "Access denied.")
        return redirect("ehealth:doctor_dashboard")
    consultation = appointment.consultation

    if request.method == "POST":
        consultation = appointment.consultation
        consultation.notes = request.POST.get("notes", "").strip()
        consultation.save()
        messages.success(request, "Notes saved successfully.")

    return redirect("ehealth:doctor_dashboard")

@login_required
def view_prescriptions(request, appointment_id):
    """
    Displays prescriptions associated with a completed consultation.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    consultation = appointment.consultation

    if request.user not in [appointment.doctor.user, appointment.patient.user]:
        return HttpResponseForbidden("Access denied")
    consultation = appointment.consultation
    prescriptions = consultation.prescriptions.all()

    return render(request,"ehealth/view_prescriptions.html", {
        "appointment": appointment,
        "prescriptions": prescriptions,
    })
