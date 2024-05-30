import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from CareSyncAI import CareSyncAI

class CareSyncApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CareSyncAI")

        self.care_sync_ai = CareSyncAI("care_sync.db")

        self.label_caregiver = tk.Label(master, text="Nom du soignant:")
        self.label_caregiver.grid(row=0, column=0, sticky="w")
        self.entry_caregiver = tk.Entry(master)
        self.entry_caregiver.grid(row=0, column=1)

        self.label_patient = tk.Label(master, text="Nom du patient:")
        self.label_patient.grid(row=1, column=0, sticky="w")
        self.entry_patient = tk.Entry(master)
        self.entry_patient.grid(row=1, column=1)

        self.label_datetime = tk.Label(master, text="Date et heure du rendez-vous (YYYY-MM-DD HH:MM:SS):")
        self.label_datetime.grid(row=2, column=0, sticky="w")
        self.entry_datetime = tk.Entry(master)
        self.entry_datetime.grid(row=2, column=1)

        self.label_duration = tk.Label(master, text="Durée du rendez-vous (en heures):")
        self.label_duration.grid(row=3, column=0, sticky="w")
        self.entry_duration = tk.Entry(master)
        self.entry_duration.grid(row=3, column=1)

        self.button_schedule = tk.Button(master, text="Planifier un rendez-vous", command=self.schedule_appointment)
        self.button_schedule.grid(row=4, columnspan=2)

        self.button_add_patient = tk.Button(master, text="Ajouter un nouveau patient", command=self.add_new_patient)
        self.button_add_patient.grid(row=5, columnspan=2)

        self.button_confirm_appointment = tk.Button(master, text="Confirmer un rendez-vous", command=self.confirm_appointment)
        self.button_confirm_appointment.grid(row=6, columnspan=2)

        self.button_cancel_appointment = tk.Button(master, text="Annuler un rendez-vous", command=self.cancel_appointment)
        self.button_cancel_appointment.grid(row=7, columnspan=2)

        self.button_show_patient_details = tk.Button(master, text="Afficher les détails d'un patient", command=self.show_patient_details)
        self.button_show_patient_details.grid(row=8, columnspan=2)

        self.button_show_appointments = tk.Button(master, text="Afficher les rendez-vous pour une date spécifique", command=self.show_appointments_for_date)
        self.button_show_appointments.grid(row=9, columnspan=2)

        self.calendar_frame = tk.Frame(master)
        self.calendar_frame.grid(row=10, columnspan=2)

    def schedule_appointment(self):
        caregiver_name = self.entry_caregiver.get().strip()
        patient_name = self.entry_patient.get().strip()
        datetime_str = self.entry_datetime.get().strip()
        duration_hours = self.entry_duration.get().strip()

        if not (caregiver_name and patient_name and datetime_str and duration_hours):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            appointment_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            duration = timedelta(hours=float(duration_hours))
            caregiver_id = self.care_sync_ai.get_caregiver_id_by_name(caregiver_name)
            patient_id = self.care_sync_ai.get_patient_id_by_name(patient_name)
            result = self.care_sync_ai.schedule_appointment(caregiver_id, patient_id, appointment_time, duration)
            messagebox.showinfo("Confirmation", result)
            self.populate_calendar(appointment_time)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def add_new_patient(self):
        # Ajoutez la logique pour ajouter un nouveau patient
        pass

    def confirm_appointment(self):
        # Ajoutez la logique pour confirmer un rendez-vous existant
        pass

    def cancel_appointment(self):
        # Ajoutez la logique pour annuler un rendez-vous existant
        pass

    def show_patient_details(self):
        # Ajoutez la logique pour afficher les détails d'un patient
        pass

    def show_appointments_for_date(self):
        # Ajoutez la logique pour afficher les rendez-vous pour une date spécifique
        pass

    def populate_calendar(self, date):
        # Ajoutez la logique pour afficher les rendez-vous sur le calendrier
        pass

def main():
    root = tk.Tk()
    app = CareSyncApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
