from toga_android import App, Activity
from toga_android.widgets import Box, Button, TextInput, TextArea, Table
import requests
import json

# Lecture du fichier de configuration JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Utilisation de l'URL du serveur à partir du fichier de configuration
server_url = config.get('server_url')

class CareSyncPatient(App):
    def startup(self):
        self.create_ui()

        # Récupérer l'ID du patient à partir de l'authentification de l'utilisateur
        patient_id = self.authenticate_user()  # Ajoutez votre logique d'authentification ici

        # Mettre à jour les rendez-vous en utilisant l'ID du patient
        self.update_appointments(patient_id)

    def create_ui(self):
        self.table = Table(
            headings=['ID', 'Date', 'Patient', 'Status'],
            on_select=self.on_row_select
        )

        self.cancel_button = Button('Annuler rendez-vous', on_press=self.cancel_appointment)
        self.move_button = Button('Déplacer rendez-vous', on_press=self.move_appointment)
        self.contact_button = Button('Contacter professionnel', on_press=self.contact_professional)

        self.email_input = TextInput(hint='Entrez email du professionnel')
        self.message_input = TextArea(hint='Entrez votre message')

        self.main_box = Box(
            children=[self.table, self.cancel_button, self.move_button, self.contact_button, self.email_input, self.message_input]
        )

        self.main_activity = Activity(
            title='My App',
            layout=self.main_box
        )

        self.main_activity.show()

    def update_appointments(self, patient_id):
        # Utiliser l'URL du serveur à partir du fichier de configuration
        server_url = config.get('server_url')

        # Construire l'URL complète pour récupérer les rendez-vous du patient spécifié
        appointments_url = f'{server_url}/upcoming-appointments/{patient_id}'

        response = requests.get(server_url)
        appointments = response.json()

        # Mettre à jour la table avec les nouveaux rendez-vous
        self.table.data = appointments

    def on_row_select(self, widget, row):
        # Cette fonction est appelée lorsque vous sélectionnez une ligne dans la table
        pass

    def cancel_appointment(self, widget):
        # Ajoutez ici la logique pour annuler un rendez-vous
        pass

    def move_appointment(self, widget):
        # Ajoutez ici la logique pour déplacer un rendez-vous
        pass

    def contact_professional(self, widget):
        email = self.email_input.value
        message = self.message_input.value
        # Ajoutez ici la logique pour contacter un professionnel de santé
        pass

if __name__ == '__main__':
    app = CareSyncPatient()
    app.main_loop()
