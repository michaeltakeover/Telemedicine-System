from django.urls import path
from .views import user_login, register_choice, register_patient, register_doctor

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register_choice, name='register'),
    path('register/patient/', register_patient, name='register_patient'),
    path('register/doctor/', register_doctor, name='register_doctor'),
]
