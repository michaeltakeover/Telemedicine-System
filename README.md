# 🩺 Telemedicine Web Application (Django)

## 📖 Project Overview
This project is a **Telemedicine Web Application** developed using **Python and Django**.  
The system enables **patients and doctors** to interact through a **secure, role-based platform** that supports:

- Appointment booking
- Consultations
- Medical records management
- Prescriptions

The application demonstrates practical implementation of:

- Django’s **MVT (Model–View–Template)** architecture
- Relational database design
- Secure authentication and authorization
- Form handling and validation
- Messaging, consultations, and audit-friendly workflows



## 🏥 Problem Domain
**Healthcare / Telemedicine**

The system addresses key challenges in modern healthcare, including:
- Managing patient–doctor interactions remotely
- Secure handling of sensitive medical data
- Appointment scheduling and consultations
- Controlled access based on defined user roles

---

## 👥 User Roles

### 👤 Patient
- Register and log in
- Book appointments
- Record vital signs
- Participate in consultations
- View prescriptions

### 👨‍⚕️ Doctor
- Approve appointments
- Conduct consultations
- Write medical notes
- Issue prescriptions
- View patient vitals

---

## 🧱 Architectural Pattern

The system follows Django’s **Model–View–Template (MVT)** architecture:

- **Models** → Define database schema and relationships  
- **Views** → Handle business logic and access control  
- **Templates** → Render HTML pages using Bootstrap  

### Benefits
- Improved maintainability
- Clear separation of concerns
- Enhanced scalability

---

## 🛠 Technologies Used

| Component        | Technology                        |
|------------------|-----------------------------------|
| Backend          | Python , Django                   |
| Frontend         | HTML5, CSS                        |
| Database         | PostgreSQL                        |
| Authentication  | Django Auth (Custom User Model)   |
| Version Control | Git & GitHub                      |

---

## 📁 Project Folder Structure

```text
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
└── communication/                    # Future extension
🔐 Security Features
Role-based access control (Patient vs Doctor)

login_required decorators

Ownership checks on appointments

CSRF protection

Server-side form validation

🧪 Testing Strategy
Manual functional testing

Django unit testing (models & forms)

Integration testing of full workflows:

Registration → Login → Dashboard

Appointment booking → Approval → Consultation

▶️ How to Run the Project
bash
Copy code
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
Then open your browser and navigate to:

text
Copy code
http://127.0.0.1:8000/