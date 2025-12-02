# creating tables

import os
import psycopg2
from dotenv import load_dotenv

# load .env variables
load_dotenv()

def DB_Operations():
    try:
        conn = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            database = os.getenv("DB_NAME"),
            password = os.getenv("DB_PASSWORD"),
            port = os.getenv("DB_PORT")
        )
        print("connected with the db server.....")
    except psycopg2.DatabaseError as e:
        print("database connection error:", e)
        return

    try:
        cur = conn.cursor()

        print("creating tables if they do not exist...")

        # ------------------ users ------------------
        cur.execute("""
            create table if not exists Users (
                user_id int generated always as identity primary key,
                full_name varchar(100) not null,
                email varchar(100) unique not null,
                password_hash varchar(200) not null,
                created_at timestamp default current_timestamp
            )
        """)

        # ------------------ roles ------------------
        cur.execute("""
            create table if not exists Roles (
                role_id int generated always as identity primary key,
                role_name varchar(20) unique not null
            )
        """)

        # ---------------- user_roles ----------------
        cur.execute("""
            create table if not exists User_roles (
                user_id int references Users(user_id),
                role_id int references Roles(role_id),
                primary key (user_id, role_id)
            )
        """)

        # ------------------ doctors ------------------
        cur.execute("""
            create table if not exists Doctors (
                doctor_id int generated always as identity primary key,
                user_id int unique references users(user_id),
                speciality varchar(100),
                license_number varchar(50),
                phone varchar(20),
                approval_status varchar(20) default 'pending'
            )
        """)

        # ------------------ patients ------------------
        cur.execute("""
            create table if not exists Patients (
                patient_id int generated always as identity primary key,
                user_id int unique references users(user_id),
                date_of_birth date,
                gender varchar(10),
                emergency_contact varchar(100)
            )
        """)

        # ---------------- appointments ----------------
        cur.execute("""
            create table if not exists Appointments (
                appointment_id int generated always as identity primary key,
                patient_id int references Patients(patient_id),
                doctor_id int references Doctors(doctor_id),
                appointment_time timestamp not null,
                reason text,
                status varchar(20) default 'pending',
                created_at timestamp default current_timestamp
            )
        """)

        # ---------------- medications ----------------
        cur.execute("""
            create table if not exists Medications (
                medication_id int generated always as identity primary key,
                medication_name varchar(100) not null,
                description text
            )
        """)

        # --------------- prescriptions ---------------
        cur.execute("""
            create table if not exists Prescriptions (
                prescription_id int generated always as identity primary key,
                appointment_id int references Appointments(appointment_id),
                patient_id int references Patients(patient_id),
                doctor_id int references Doctors(doctor_id),
                issued_at timestamp default current_timestamp
            )
        """)

        # ----------- prescription_items --------------
        cur.execute("""
            create table if not exists Prescription_items (
                item_id int generated always as identity primary key,
                prescription_id int references Prescriptions(prescription_id),
                medication_id int references Medications(medication_id),
                dosage varchar(50),
                frequency varchar(50),
                duration varchar(50)
            )
        """)

        # ------------------- vitals -------------------
        cur.execute("""
            create table if not exists Vitals (
                vitals_id int generated always as identity primary key,
                patient_id int not null references Patients(patient_id),
                appointment_id int references Appointments(appointment_id),
                weight numeric(5,2),
                temperature numeric(4,1),
                heart_rate int,
                blood_pressure varchar(20),
                recorded_at timestamp default current_timestamp
            )
        """)

        # ---------------- notifications ---------------
        cur.execute("""
            create table if not exists Notifications (
                notification_id int generated always as identity primary key,
                user_id int references Users(user_id),
                message text not null,
                is_read boolean default false,
                created_at timestamp default current_timestamp
            )
        """)

        conn.commit()
        print("All tables created successfully!")

    except psycopg2.DatabaseError as e:
        print("Error executing table commands:", e)

    conn.close()


def main():
    print("- - - working with postgresql db - - -")
    DB_Operations()


if __name__ == "__main__":
    main()
