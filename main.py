import tkinter as tk
from CareSyncApp import CareSyncApp
from CareSyncAI import CareSyncAI
from VirtualPlanningAssistant import VirtualPlanningAssistant, DatabaseManager

def simulate_virtual_assistant():
    db_manager = DatabaseManager("care_sync.db")
    virtual_planning_assistant = VirtualPlanningAssistant(db_manager)

    # Simuler l'ajout d'un nouveau patient
    patient_id = db_manager.add_patient("Jeanne Dupont", "Historique médical", "Médicaments", "Allergies", "Contacts d'urgence")

    # Simuler la planification automatique d'un rendez-vous pour le nouveau patient
    appointment_id = virtual_planning_assistant.auto_schedule_appointment(patient_id)

    # Simuler l'envoi d'une confirmation de rendez-vous
    virtual_planning_assistant.send_confirmation(appointment_id)

    # Simuler l'annulation du rendez-vous et la proposition d'une nouvelle date
    virtual_planning_assistant.handle_cancellation(appointment_id)

def main():
    # Lancement de l'interface utilisateur
    root = tk.Tk()
    app = CareSyncApp(root)

    # Simuler l'Assistant Virtuel de Planification avant de lancer l'interface utilisateur
    simulate_virtual_assistant()

    # Initialisation de la base de données et des gestionnaires après la simulation
    db_name = "care_sync.db"
    care_sync_ai = CareSyncAI(db_name)
    virtual_planning_assistant = VirtualPlanningAssistant(DatabaseManager(db_name))

    # Attribution des objets care_sync_ai et virtual_planning_assistant à l'application
    app.care_sync_ai = care_sync_ai
    app.virtual_planning_assistant = virtual_planning_assistant

    root.mainloop()

if __name__ == "__main__":
    main()
