from django.urls import path

# basic pages
from .views.home import home
from .views.support import support

# authentication
from .views.auth import (
    user_login,
    register,
    activate_account,
)

# patient
from .views.patient import (
    patient_dashboard,
    book_appointment,
    add_vitals,
)

# doctor
from .views.doctor import (
    doctor_dashboard,
    complete_appointment,
)

# appointments (doctor actions)
from .views.appointments import (
    approve_appointment,
    doctor_appointment_detail,
)

# consultation & prescriptions
from .views.consultation import ( consultation_chat,  create_prescription, save_notes,view_prescriptions,)

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


    path("appointments/book/", book_appointment, name="book_appointment"),
    path("vitals/add/", add_vitals, name="add_vitals"),

    # doctor actions
    path( "appointments/approve/<uuid:appointment_id>/", approve_appointment, name="approve_appointment",),
    path("appointments/complete/<uuid:appointment_id>/",complete_appointment,name="complete_appointment",),
    path( "appointments/<uuid:appointment_id>/detail/", doctor_appointment_detail, name="doctor_appointment_detail", ),


    path("appointments/<uuid:appointment_id>/chat/", consultation_chat,name="consultation_chat", ),
    path("appointments/<uuid:appointment_id>/prescription/add/",create_prescription, name="create_prescription", ),
    path("appointments/<uuid:appointment_id>/notes/", save_notes,name="save_notes" ),
    path("appointments/<uuid:appointment_id>/prescriptions/",view_prescriptions,name="view_prescriptions",),
]
