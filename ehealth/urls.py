from django.urls import path
from .views.home import home
from .views.support import support
from .views.auth import (user_login, register,activate_account,)
from .views.patient import (patient_dashboard,book_appointment,add_vitals,)
# doctor
from .views.doctor import (doctor_dashboard, complete_appointment)
from .views.appointments import (approve_appointment,doctor_appointment_detail,cancel_appointment)
# consultation & prescriptions
from .views.consultation import ( consultation_chat,  create_prescription, save_notes,view_prescriptions,view_vitals)

app_name = "ehealth"

urlpatterns = [
    # public
    path("", home, name="home"),
    path("support/", support, name="support"),

    # auth
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("activate/<uid>/<token>/", activate_account, name="activate"),

    # dashboards
    path("dashboard/patient/", patient_dashboard, name="patient_dashboard"),
    path("dashboard/doctor/", doctor_dashboard, name="doctor_dashboard"),
    path("doctor/appointment/<uuid:appointment_id>/",doctor_appointment_detail,name="doctor_appointment_detail"),
    path("doctor/patient/<uuid:patient_id>/vitals/",view_vitals,name="view_vitals"),


    path("appointments/book/", book_appointment, name="book_appointment"),
    path("vitals/add", add_vitals, name="add_vitals"),
    path("vitals/",view_vitals,name="view_vitals"),


    path( "appointments/approve/<uuid:appointment_id>/", approve_appointment, name="approve_appointment",),
    path("appointments/complete/<uuid:appointment_id>/",complete_appointment,name="complete_appointment",),
    path( "appointments/<uuid:appointment_id>/detail/", doctor_appointment_detail, name="doctor_appointment_detail", ),


    path("appointments/<uuid:appointment_id>/chat/", consultation_chat,name="consultation_chat", ),
    path("appointments/<uuid:appointment_id>/prescription/add/",create_prescription, name="create_prescription", ),
    path("appointments/<uuid:appointment_id>/notes/", save_notes,name="save_notes" ),
    path("appointments/<uuid:appointment_id>/prescriptions/",view_prescriptions,name="view_prescriptions",),
    path("appointments/<uuid:appointment_id>/cancel/", cancel_appointment, name="cancel_appointment")





]
