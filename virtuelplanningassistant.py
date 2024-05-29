import sqlite3
from datetime import datetime, timedelta
import random

class VirtualPlanningAssistant:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def auto_schedule_appointment(self, patient_id):
        now = datetime.now()
        random_days = timedelta(days=random.randint(1, 7))
        random_hours = timedelta(hours=random.randint(8, 17))
        appointment_time = (now + random_days + random_hours).replace(minute=0, second=0)
        appointment_duration = timedelta(hours=1)
        caregiver_id = random.choice(self.db_manager.get_caregivers())['id']
        return self.db_manager.schedule_appointment(caregiver_id, patient_id, appointment_time, appointment_duration)

    def send_confirmation(self, appointment_id):
        print(f"Rendez-vous ID {appointment_id} confirmé avec le patient.")

    def handle_cancellation(self, appointment_id):
        self.db_manager.cancel_appointment(appointment_id)
        print(f"Rendez-vous ID {appointment_id} annulé. Proposition d'une nouvelle date.")

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
                            appointment_time TEXT, duration TEXT, confirmed BOOLEAN)''')
        self.conn.commit()

    def schedule_appointment(self, caregiver_id, patient_id, appointment_time, appointment_duration):
        try:
            appointment_time_str = appointment_time.strftime("%Y-%m-%d %H:%M:%S")
            duration_str = str(appointment_duration.total_seconds())
            self.cur.execute("INSERT INTO appointments (caregiver_id, patient_id, appointment_time, duration, confirmed) \
            VALUES (?, ?, ?, ?, ?)", (caregiver_id, patient_id, appointment_time_str, duration_str, False))
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def cancel_appointment(self, appointment_id):
        try:
            self.cur.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_caregivers(self):
        try:
            self.cur.execute("SELECT * FROM caregivers")
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    db_manager = DatabaseManager("care_sync.db")
    assistant = VirtualPlanningAssistant(db_manager)
    # Exemples d'utilisation de l'assistant
    patient_id = 1  # ID d'un patient existant
    appointment_id = assistant.auto_schedule_appointment(patient_id)
    assistant.send_confirmation(appointment_id)
