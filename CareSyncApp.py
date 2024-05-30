"""
CareSyncApp.py: Ce module gère l'interface utilisateur de l'application de synchronisation des soins.
"""
import os
import sqlite3
import json
import requests
import tkinter as tk
import tkinter.ttk as ttk  # Importez ttk
from tkinter import messagebox, OptionMenu
from datetime import datetime, timedelta
from tkcalendar import Calendar, DateEntry
import random
from PIL import ImageTk, Image
from DatabaseManager import DatabaseManager

class CareSyncApp:
    def __init__(self, master, db_name):
        self.master = master
        self.master.title("CareSyncAI")
        self.db_manager = DatabaseManager(db_name)
        
        # Définir la taille de la fenêtre sur la taille maximale de l'écran
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        self.master.geometry(f"{width}x{height}")

        # Cadre pour la barre de tâches
        self.frame_status_bar = tk.LabelFrame(master, text="Notes")
        self.frame_status_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Ajouter un widget Text pour afficher les Notes
        self.message_display = tk.Text(self.frame_status_bar, height=10, width=100)
        self.message_display.pack(fill="both", expand=True)
        
        # Chargement de l'image du logo
        logo_img = Image.open("./images/logo.jpg")
        logo_img = logo_img.resize((550, 550), Image.LANCZOS)  # Utilisez LANCZOS pour le redimensionnement
        self.logo = ImageTk.PhotoImage(logo_img)

        # Afficher le logo dans un label
        self.logo_label = tk.Label(master, image=self.logo)
        self.logo_label.place(x=950, y=1)  # Position absolue du logo (20, 20)
        

        specialties = [
            "Médecine générale",
            "Médecine du sport",
            "Médecine du travail",
            "Médecine légale",
            "Médecine physique et de réadaptation",
            "Addictologie",
            "Algologie",
            "Allergologie",
            "Anesthésie-Réanimation",
            "Cancérologie",
            "Cardio-vasculaire HTA",
            "Chirurgie",
            "Dermatologie",
            "Diabétologie-Endocrinologie",
            "Génétique",
            "Gériatrie",
            "Gynécologie-Obstétrique",
            "Hématologie",
            "Hépato-gastro-entérologie",
            "Imagerie médicale",
            "Immunologie",
            "Infectiologie",
            "Néphrologie",
            "Neurologie",
            "Nutrition",
            "Ophtalmologie",
            "ORL",
            "Pédiatrie",
            "Pneumologie",
            "Psychiatrie",
            "Radiologie",
            "Rhumatologie",
            "Sexologie",
            "Toxicologie",
            "Urologie"
        ]

        # Cadre pour les informations du professionnel de santé
        self.frame_professional = tk.LabelFrame(master, text="Informations du professionnel de santé")
        self.frame_professional.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
       
        # Créez la liste déroulante pour la civilité
        self.label_prefix = tk.Label(self.frame_professional, text="Civilité:")
        self.label_prefix.grid(row=0, column=0, sticky="w")

        # Définissez self.selected_prefix comme une variable de chaîne vide dans le constructeur de CareSyncApp
        self.selected_prefix = tk.StringVar()
        self.selected_prefix.set("")  # Définissez la valeur par défaut du menu déroulant
        self.combo_prefix = OptionMenu(self.frame_professional, self.selected_prefix, *["M.", "Mme","Docteur"])
        self.combo_prefix.grid(row=0, column=1)

        self.label_last_name = tk.Label(self.frame_professional, text="Nom:")
        self.label_last_name.grid(row=1, column=0, sticky="w")
        self.entry_last_name = tk.Entry(self.frame_professional, width=40)
        self.entry_last_name.grid(row=1, column=1, sticky="w")

        self.label_first_name = tk.Label(self.frame_professional, text="Prénom:")
        self.label_first_name.grid(row=2, column=0, sticky="w")
        self.entry_first_name = tk.Entry(self.frame_professional, width=40)
        self.entry_first_name.grid(row=2, column=1)

        self.label_rpps = tk.Label(self.frame_professional, text="RPPS:")
        self.label_rpps.grid(row=3, column=0, sticky="w")
        self.entry_rpps = tk.Entry(self.frame_professional, width=11)
        self.entry_rpps.grid(row=3, column=1, sticky="w")

        self.label_specialty = tk.Label(self.frame_professional, text="Spécialité:")
        self.label_specialty.grid(row=4, column=0, sticky="w")

        # Définissez self.selected_specialty comme une variable de chaîne vide dans le constructeur de CareSyncApp
        self.selected_specialty = tk.StringVar()
        self.selected_specialty.set("")  # Définissez la valeur par défaut du menu déroulant
        self.combo_specialty = OptionMenu(self.frame_professional, self.selected_specialty, *specialties)
        self.combo_specialty.grid(row=4, column=1)

        self.button_add_professional = tk.Button(self.frame_professional, text="Ajouter un professionnel", command=self.add_health_professional)
        self.button_add_professional.grid(row=5, columnspan=2)

        # Cadre pour les informations du patient
        self.frame_patient = tk.LabelFrame(master, text="Informations du patient")
        self.frame_patient.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.label_patient_prefix = tk.Label(self.frame_patient, text="Civilité:")
        self.label_patient_prefix.grid(row=0, column=0, sticky="w")
        self.selected_patient_prefix = tk.StringVar()
        self.combo_patient_prefix = ttk.Combobox(self.frame_patient, textvariable=self.selected_patient_prefix, state="readonly")
        self.combo_patient_prefix['values'] = ('M.', 'Mme', 'Dr')
        self.combo_patient_prefix.grid(row=0, column=1)

        self.label_patient_name = tk.Label(self.frame_patient, text="Nom:")
        self.label_patient_name.grid(row=1, column=0, sticky="w")
        self.entry_patient_name = tk.Entry(self.frame_patient, width=40)
        self.entry_patient_name.grid(row=1, column=1, sticky="w")

        self.label_patient_first_name = tk.Label(self.frame_patient, text="Prénom:")
        self.label_patient_first_name.grid(row=2, column=0, sticky="w")
        self.entry_patient_first_name = tk.Entry(self.frame_patient, width=40)
        self.entry_patient_first_name.grid(row=2, column=1, sticky="w")

        self.label_patient_dob = tk.Label(self.frame_patient, text="Date de naissance:")
        self.label_patient_dob.grid(row=3, column=0, sticky="w")
        self.entry_patient_dob = DateEntry(self.frame_patient, date_pattern="dd-mm-yyyy", width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_patient_dob.grid(row=3, column=1)

        self.label_patient_sex = tk.Label(self.frame_patient, text="Sexe:")
        self.label_patient_sex.grid(row=4, column=0, sticky="w")
        self.selected_sex = tk.StringVar()
        self.combo_sex = ttk.Combobox(self.frame_patient, textvariable=self.selected_sex, state="readonly")
        self.combo_sex['values'] = ('Masculin', 'Féminin')
        self.combo_sex.grid(row=4, column=1)

        self.label_patient_place_of_birth = tk.Label(self.frame_patient, text="Lieu de naissance:")
        self.label_patient_place_of_birth.grid(row=5, column=0, sticky="w")
        self.entry_patient_place_of_birth = tk.Entry(self.frame_patient, width=35)
        self.entry_patient_place_of_birth.grid(row=5, column=1)

        self.label_patient_social_security_number = tk.Label(self.frame_patient, text="Numéro de sécurité sociale:")
        self.label_patient_social_security_number.grid(row=6, column=0, sticky="w")
        self.entry_patient_social_security_number = tk.Entry(self.frame_patient, width=15)
        self.entry_patient_social_security_number.grid(row=6, column=1)


        self.button_add_patient = tk.Button(self.frame_patient, text="Ajouter un patient", command=self.add_patient)
        self.button_add_patient.grid(row=7, columnspan=2)

        # Cadre pour le rendez-vous
        self.frame_appointment = tk.LabelFrame(master, text="Rendez-vous")
        self.frame_appointment.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.label_datetime = tk.Label(self.frame_appointment, text="Date:")
        self.label_datetime.grid(row=0, column=0, sticky="w")
        self.entry_date = DateEntry(self.frame_appointment, date_pattern="dd-mm-yyyy", width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_date.grid(row=0, column=1)

        self.label_time = tk.Label(self.frame_appointment, text="Heure:")
        self.label_time.grid(row=1, column=0, sticky="w")
        self.entry_time = tk.Entry(self.frame_appointment)
        self.entry_time.grid(row=1, column=1)

        self.label_duration = tk.Label(self.frame_appointment, text="Durée:")
        self.label_duration.grid(row=2, column=0, sticky="w")
        self.entry_duration = tk.Entry(self.frame_appointment)
        self.entry_duration.grid(row=2, column=1)

        self.button_schedule = tk.Button(self.frame_appointment, text="Planifier un rendez-vous", command=self.schedule_appointment)
        self.button_schedule.grid(row=3, columnspan=2)


    def validate_name(self, name):
        return name.isalpha()
    
    def show_calendar(self, event):
        # Affichage du calendrier lorsque le champ de saisie est cliqué
        top = tk.Toplevel(self.master)
        cal = Calendar(top, selectmode="day", date_pattern="dd-mm-yyyy")
        cal.pack(padx=10, pady=10)

        # Bouton "Valider" pour sélectionner la date
        validate_button = tk.Button(top, text="Valider", command=lambda: self.select_date_time(cal))
        validate_button.pack(pady=10)

    def select_date_time(self, calendar):
        # Mettre à jour le champ de saisie avec la date sélectionnée dans le calendrier
        selected_date = calendar.get_date()
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, selected_date)

    def add_health_professional(self):
        prefix = self.selected_prefix.get().strip()
        first_name = self.entry_first_name.get().strip()
        last_name = self.entry_last_name.get().strip()
        rpps = self.entry_rpps.get().strip()
        specialty = self.selected_specialty.get().strip()  # Modifier cette ligne

        if not (prefix and first_name and last_name and rpps and specialty):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            rpps = int(rpps)
            professional_id = self.db_manager.add_health_professional(prefix, first_name, last_name, rpps, specialty)
            messagebox.showinfo("Confirmation", "Professionnel de santé ajouté avec succès. ID: {}".format(professional_id))
        except ValueError:
            messagebox.showerror("Erreur", "RPPS doit être un nombre entier.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Ce numéro RPPS existe déjà dans la base de données. Veuillez vérifier les données saisies.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def schedule_appointment(self):
        patient_name = self.entry_patient_name.get().strip()
        date_str = self.entry_date.get().strip()
        time_str = self.entry_time.get().strip()
        duration_hours = self.entry_duration.get().strip()

        if not patient_name:
            messagebox.showerror("Erreur", "Veuillez entrer le nom du patient.")
            return

        if not (date_str and time_str and duration_hours):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            appointment_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M:%S")
            appointment_duration = timedelta(hours=int(duration_hours))
            self.db_manager.schedule_appointment(1, 1, appointment_time, appointment_duration)  # Remplacer 1, 1 par les vrais IDs de professionnel et de patient
            messagebox.showinfo("Confirmation", "Rendez-vous planifié avec succès.")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date ou d'heure invalide.")
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

    def add_patient(self):
         # Lecture du fichier de configuration JSON
        config_path = os.path.join(os.getcwd(), 'conf', 'config.json')
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
       

        name = self.entry_patient_name.get().strip()
        first_name = self.entry_patient_first_name.get().strip()
        date_of_birth = self.entry_patient_dob.get().strip()  # Assurez-vous que vous obtenez la date de naissance au format correct
        sex = self.combo_sex.get().strip()  # Obtenez la valeur sélectionnée dans la combobox
        prefix = self.combo_patient_prefix.get().strip()  # Obtenez la valeur sélectionnée dans la combobox
        place_of_birth = self.entry_patient_place_of_birth.get().strip()
        social_security_number = self.entry_patient_social_security_number.get().strip()
        medical_history = ""  # Ajoutez la logique pour obtenir l'historique médical
        medications = ""  # Ajoutez la logique pour obtenir les médicaments
        allergies = ""  # Ajoutez la logique pour obtenir les allergies
        emergency_contacts = ""  # Ajoutez la logique pour obtenir les contacts d'urgence

        # Validation des données obligatoires
        if not all([name, first_name, date_of_birth, sex, prefix, place_of_birth, social_security_number]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        try:
            # Convertir la date de naissance en objet datetime
            date_of_birth_obj = datetime.strptime(date_of_birth, '%d-%m-%Y')
            # Formater la date de naissance en ISO 8601
            date_of_birth_iso = date_of_birth_obj.strftime('%Y-%m-%d')

            # Préparez les données pour l'API
            patient_data = {
                "name": name,
                "first_name": first_name,
                "date_of_birth": date_of_birth_iso,  # Utilisez la date de naissance formatée
                "sex": sex,
                "prefix": prefix,
                "place_of_birth": place_of_birth,
                "social_security_number": social_security_number,
                # Ajoutez d'autres données si nécessaire
            }

            # URL de l'API de création de patient
             # Récupération de l'adresse URL et du port de l'API de création de patient
            api_url = f"http://{config.get('http_url')}:{config.get('port')}/add_patient"

            # Envoyer la requête POST à l'API
            response = requests.post(api_url, json=patient_data)

            # Vérifier le code de statut de la réponse
            if response.ok:
                # Afficher un message de succès
                messagebox.showinfo("Succès", "Patient ajouté avec succès.")
            else:
                # Afficher un message d'erreur avec le code de statut de la réponse
                messagebox.showerror("Erreur", f"Erreur {response.status_code} lors de l'ajout du patient: {response.text}")

        except Exception as e:
            # Afficher un message d'erreur détaillé
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'ajout du patient: {e}")
