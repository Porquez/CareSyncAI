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