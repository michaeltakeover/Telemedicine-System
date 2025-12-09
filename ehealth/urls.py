# ehealth/urls.py

from django.urls import path
from  .import views


#app_name = 'ehealth'

urlpatterns = [

    #path('admin/', admin.site.urls, name='admin.site.urls'),
    # path('home/', views.home),
    path('login/', views.user_login, name='login'),
    path('Support/',views.Support, name='Support'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path("activate/<uid>/<token>/", views.activate_account, name="activate"),
    path("dashboard/patient/", views.patient_dashboard, name="patient_dashboard"),
    path("dashboard/doctor/", views.doctor_dashboard, name="doctor_dashboard"),




]