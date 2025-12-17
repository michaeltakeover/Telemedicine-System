Telemedicine Web Application (Django)
Project Overview

This project is a Telemedicine Web Application developed using Python and Django.
The system enables patients and doctors to interact through a secure, role-based platform that supports appointment booking, consultations, medical records, and prescriptions.

The application demonstrates the use of:

Django’s MVT (Model–View–Template) architecture

Relational database design

Secure authentication and authorization

Form handling and validation

Messaging, consultations, and audit-friendly workflows

This project was developed as part of a Master’s level Continuous Assessment (CA2).

Problem Domain

Healthcare / Telemedicine

The system addresses the challenge of:

Managing patient–doctor interactions remotely

Secure handling of medical data

Appointment scheduling and consultations

Controlled access based on user roles

User Roles

Patient

Register and log in

Book appointments

Record vital signs

Participate in consultations

View prescriptions

Doctor

Approve appointments

Conduct consultations

Write medical notes

Issue prescriptions

View patient vitals

Architectural Pattern

The system follows the Model–View–Template (MVT) pattern provided by Django:

Models → Define database schema and relationships

Views → Handle business logic and access control

Templates → Render HTML pages using Bootstrap

This layered approach improves:

Maintainability

Separation of concerns

Scalability

 Technologies Used
Component	Technology
Backend	Python 3, Django
Frontend	HTML5,CSS
Database	PostgreSQL 
Authentication	Django Auth (custom user model)

Version Control	Git & GitHub
Project Folder Structure
CA2-PROGRAMMING/
│
├── manage.py
├── README.md
├── .env
├── .gitignore
│
├── telemedicine/                     # Django project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── ehealth/                          # Main Django application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── signals.py
│   ├── urls.py
│
│   ├── models/                       # Database models (data layer)
│   │   ├── __init__.py
│   │   ├── accounts.py               # Custom user model
│   │   ├── patient.py                # Patient profile
│   │   ├── doctor.py                 # Doctor profile
│   │   ├── communication.py          # Chat / consultation models
│   │   └── records.py                # Medical records & vitals
│
│   ├── forms/                        # Django forms (validation layer)
│   │   ├── __init__.py
│   │   ├── auth.py                   # Registration & login forms
│   │   ├── appointment.py            # Appointment booking form
│   │   ├── vitals.py                 # Vital signs form
│   │   └── prescription.py           # Prescription form
│
│   ├── views/                        # Business logic (controller layer)
│   │   ├── __init__.py
│   │   ├── auth.py                   # Authentication views
│   │   ├── patient.py                # Patient workflows
│   │   ├── doctor.py                 # Doctor workflows
│   │   ├── appointments.py           # Appointment management
│   │   ├── consultation.py           # Chat & consultation logic
│   │   ├── home.py                   # Home page view
│   │   └── support.py                # Support page view
│
│   ├── templates/
│   │   └── ehealth/                  # HTML templates (presentation layer)
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── patient_dashboard.html
│   │       ├── doctor_dashboard.html
│   │       ├── book_appointment.html
│   │       ├── add_vitals.html
│   │       ├── consultation_chat.html
│   │       ├── create_prescription.html
│   │       ├── view_prescriptions.html
│   │       ├── navbar.html
│   │       ├── footer.html
│   │       ├── main.html
│   │       └── support.html
│
│   ├── tests/                        # Testing layer
│   │   ├── __init__.py
│   │   ├── test_models.py             # Model unit tests
│   │   ├── test_forms.py              # Form tests
│   │   ├── test_views.py              # View tests
│   │   └── integration_tests.py       # End-to-end tests
│
│   ├── migrations/
│   └── __pycache__/
│
└── communication/                     future extension

 Security Features

Role-based access control (Patient vs Doctor)

Login required decorators

Ownership checks on appointments

CSRF protection

Server-side form validation

Testing Strategy

Manual functional testing

Django unit testing (models & forms)

Integration testing of workflows:

Registration → Login → Dashboard

Appointment booking → Approval → Consultation

How to Run the Project
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver


Then open:

http://127.0.0.1:8000/
