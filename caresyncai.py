import sqlite3
from datetime import datetime, timedelta
import random

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS caregivers
                            (id INTEGER PRIMARY KEY, name TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS patients
                            (id INTEGER PRIMARY KEY, name TEXT, medical_history TEXT, medications TEXT, allergies TEXT, emergency_contacts TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS appointments
                            (id INTEGER PRIMARY KEY, caregiver_id INTEGER, patient_id INTEGER, 
                            appointment_time TEXT, duration INTEGER, confirmed BOOLEAN)''')
        self.conn.commit()

    def add_caregiver(self, name):
        try:
            self.cur.execute("INSERT INTO caregivers (name) VALUES (?)", (name,))
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def add_patient(self, name, medical_history, medications, allergies, emergency_contacts):
        try:
            self.cur.execute("INSERT INTO patients (name, medical_history, medications, allergies, emergency_contacts) \
            VALUES (?, ?, ?, ?, ?)", (name, medical_history, medications, allergies, emergency_contacts))
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def schedule_appointment(self, caregiver_id, patient_id, appointment_time, appointment_duration):
        try:
            appointment_time_str = appointment_time.strftime("%Y-%m-%d %H:%M:%S")
            duration_str = str(appointment_duration.total_seconds())  # Convertir en secondes
            self.cur.execute("INSERT INTO appointments (caregiver_id, patient_id, appointment_time, duration, confirmed) \
            VALUES (?, ?, ?, ?, ?)", (caregiver_id, patient_id, appointment_time_str, duration_str, False))
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

class CareSyncAI:
    def __init__(self, db_name):
        self.db_manager = DatabaseManager(db_name)

    def add_caregiver(self, name):
        return self.db_manager.add_caregiver(name)

    def add_patient(self, name, medical_history, medications, allergies, emergency_contacts):
        return self.db_manager.add_patient(name, medical_history, medications, allergies, emergency_contacts)

    def schedule_appointment(self, caregiver_id, patient_id, appointment_time, appointment_duration):
        appointment_id = self.db_manager.schedule_appointment(caregiver_id, patient_id, appointment_time, appointment_duration)
        return f"Rendez-vous programmé avec succès. ID: {appointment_id}"

    def confirm_appointment(self, appointment_id):
        self.db_manager.confirm_appointment(appointment_id)
        return "Rendez-vous confirmé."

    def cancel_appointment(self, appointment_id):
        self.db_manager.cancel_appointment(appointment_id)
        return "Rendez-vous annulé avec succès."

    def get_patient_details(self, patient_id):
        return self.db_manager.get_patient_details(patient_id)

    def get_appointments_for_date(self, date):
        return self.db_manager.get_appointments_for_date(date)


if __name__ == "__main__":
    care_sync_ai = CareSyncAI("care_sync.db")
    # Autres opérations de test
