"""
CareSyncAI.py: Ce module gére les fonctionnalités liées a la synchronisation des soins.
"""
from DatabaseManager import DatabaseManager

class CareSyncAI:
    def __init__(self, db_name):
        self.db_manager = DatabaseManager(db_name)

    def add_caregiver(self, name):
        return self.db_manager.add_caregiver(name)

    def add_patient(self, name, first_name, date_of_birth, sex, prefix, place_of_birth, social_security_number, 
                    medical_history, medications, allergies, emergency_contacts):
        return self.db_manager.add_patient(name, first_name, date_of_birth, sex, prefix, place_of_birth, 
                                           social_security_number, medical_history, medications, allergies, emergency_contacts)

    def schedule_appointment(self, caregiver_id, patient_id, appointment_time, appointment_duration):
        appointment_id = self.db_manager.schedule_appointment(caregiver_id, patient_id, appointment_time, appointment_duration)
        return f"Rendez-vous programme avec succès. ID: {appointment_id}"

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

