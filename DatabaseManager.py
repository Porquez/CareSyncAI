# file: database_manager.py
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS caregivers
                            (id INTEGER PRIMARY KEY, name TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS patients
                            (id INTEGER PRIMARY KEY, name TEXT, first_name TEXT, date_of_birth TEXT, sex TEXT, prefix TEXT, 
                            place_of_birth TEXT, social_security_number TEXT, medical_history TEXT, medications TEXT, 
                            allergies TEXT, emergency_contacts TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS appointments
                            (id INTEGER PRIMARY KEY, caregiver_id INTEGER, health_professional_id INTEGER, patient_id INTEGER, 
                            appointment_time TEXT, duration TEXT, confirmed BOOLEAN)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS health_professionals
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, prefix TEXT, first_name TEXT, last_name TEXT, rpps INTEGER UNIQUE, 
                            name TEXT, specialty TEXT)''')
        self.conn.commit()

    def add_caregiver(self, name):
        try:
            self.cur.execute("INSERT INTO caregivers (name) VALUES (?)", (name,))
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def add_patient(self, name, first_name, date_of_birth, sex, prefix, place_of_birth, social_security_number, 
                    medical_history, medications, allergies, emergency_contacts):
        try:
            self.cur.execute("INSERT INTO patients (name, first_name, date_of_birth, sex, prefix, place_of_birth, social_security_number, \
            medical_history, medications, allergies, emergency_contacts) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, first_name, date_of_birth, sex, prefix, place_of_birth, 
                                                       social_security_number, medical_history, medications, allergies, 
                                                       emergency_contacts))
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def add_health_professional(self, prefix, first_name, last_name, rpps, specialty):
        try:
            name = f"{prefix} {first_name} {last_name}"
            self.cur.execute("INSERT INTO health_professionals (prefix, first_name, last_name, rpps, name, specialty) \
            VALUES (?, ?, ?, ?, ?, ?)", (prefix, first_name, last_name, rpps, name, specialty))
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def check_conflicts(self, professional_id, appointment_time, appointment_duration):
        duration_seconds = int(appointment_duration.total_seconds())
        appointment_end_time = appointment_time + timedelta(seconds=duration_seconds)
        self.cur.execute('''
        SELECT * FROM appointments WHERE caregiver_id = ? AND (
        (appointment_time < ? AND datetime(appointment_time, '+' || duration || ' seconds') > ?)
        )
        ''', (professional_id, appointment_end_time, appointment_time))
        return self.cur.fetchall()
        
    
    def schedule_appointment(self, professional_id, patient_id, appointment_time, appointment_duration):
        try:
            conflicts = self.check_conflicts(professional_id, appointment_time, appointment_duration)
            if conflicts:
                return "Conflit d�tect� avec d'autres rendez-vous. Veuillez choisir un autre cr�neau horaire."
            appointment_time_str = appointment_time.strftime("%Y-%m-%d %H:%M:%S")
            duration_str = str(int(appointment_duration.total_seconds()))
            self.cur.execute("INSERT INTO appointments (caregiver_id, patient_id, appointment_time, duration, confirmed) \
            VALUES (?, ?, ?, ?, ?)", (professional_id, patient_id, appointment_time_str, duration_str, False))
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
        
    def confirm_appointment(self, appointment_id):
        try:
            self.cur.execute("UPDATE appointments SET confirmed = ? WHERE id = ?", (True, appointment_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def cancel_appointment(self, appointment_id):
        try:
            self.cur.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_patient_details(self, patient_id):
        try:
            self.cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            return self.cur.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_appointments_for_date(self, date):
        try:
            start_date_str = date.strftime("%Y-%m-%d 00:00:00")
            end_date_str = date.strftime("%Y-%m-%d 23:59:59")
            self.cur.execute("SELECT * FROM appointments WHERE appointment_time BETWEEN ? AND ?", (start_date_str, end_date_str))
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def close_connection(self):
        self.cur.close()
        self.conn.close()
