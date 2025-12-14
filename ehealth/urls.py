# ehealth/urls.py

from django.urls import path
from  .import views


#app_name = 'ehealth'

urlpatterns = [

    #path('admin/', admin.site.urls, name='admin.site.urls'),
    # path('home/', views.home),
    path('login/', views.user_login, name='login'),
    path('support/',views.support, name='support'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path("activate/<uid>/<token>/", views.activate_account, name="activate"),
    path("dashboard/patient/", views.patient_dashboard, name="patient_dashboard"),
    path("dashboard/doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path("appointments/book/", views.book_appointment, name="book_appointment"),
    path("appointments/approve/<uuid:appointment_id>/",views.approve_appointment,name="approve_appointment" ),
    path("appointments/complete/<uuid:appointment_id>/", views.complete_appointment,name="complete_appointment"),
    path("vitals/add/", views.add_vitals, name="add_vitals" ),
    path("appointments/<uuid:appointment_id>/chat/",views.consultation_chat,name="consultation_chat"),
    path("appointments/<uuid:appointment_id>/prescription/add/", views.create_prescription,name="create_prescription"),
    path("appointments/<uuid:appointment_id>/notes/", views.save_notes, name="save_notes"),
    path("appointments/<uuid:appointment_id>/prescriptions/",views.view_prescriptions, name="view_prescriptions"),
    path("appointments/<uuid:appointment_id>/save-notes/",views.save_notes,name="save_notes"),








  ]