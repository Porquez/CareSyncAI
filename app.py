import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Chemin complet vers le répertoire contenant le fichier de base de données
db_dir = '/home/syst/CareSyncAI'

# Nom du fichier de base de données
db_filename = 'care_sync.db'

# Chemin complet vers le fichier de base de données
db_path = os.path.join(db_dir, db_filename)

app = Flask(__name__)
# Configuration de l'URI de base de données avec le chemin complet
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)
print(app.config['SQLALCHEMY_DATABASE_URI'])

# Configuration de la journalisation
logging.basicConfig(level=logging.DEBUG)  # Définir le niveau de journalisation sur DEBUG

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime)
    sex = db.Column(db.String(10))
    prefix = db.Column(db.String(10))
    place_of_birth = db.Column(db.String(100))
    social_security_number = db.Column(db.String(15))
    medical_history = db.Column(db.String(100))
    medications = db.Column(db.String(100))
    emergency_contacts= db.Column(db.String(100))
    allergies = db.Column(db.String(100))

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))

# Route pour afficher la liste des rendez-vous des patients
@app.route('/appointments')
def list_appointments():
    logging.debug('Accès à la liste des rendez-vous des patients')
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

def convert_date_of_birth(date_string):
    try:
        # Utiliser strptime pour convertir la chaîne en objet datetime
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%d-%m-%Y')  # Format en 'DD-MM-YYYY'
    except ValueError:
        try:
            # Si la conversion échoue, essayez un autre format
            date_obj = datetime.strptime(date_string, '%d-%m-%Y')
            return date_obj.strftime('%d-%m-%Y')  # Format en 'DD-MM-YYYY'
        except ValueError:
            # Si les deux conversions échouent, renvoyez None ou une valeur par défaut
            return None


# Route pour ajouter un patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        name = request.form.get('name')
        first_name = request.form.get('first_name')
        date_of_birth = request.form.get('date_of_birth')
        sex = request.form.get('sex')
        prefix = request.form.get('prefix')
        place_of_birth = request.form.get('place_of_birth')
        social_security_number = request.form.get('social_security_number')
        medical_history = request.form.get('medical_history')
        medications = request.form.get('medications')
        allergies = request.form.get('allergies')
        emergency_contacts = request.form.get('emergency_contacts')
        
        # Ajoutez ici la logique pour valider les données et les enregistrer dans la base de données
        
        # Exemple de réponse JSON
        return jsonify({'message': 'Patient ajouté avec succès'}), 201
    else:
        return jsonify({'error': 'Méthode non autorisée'}), 405

# Route pour afficher la liste des patients
@app.route('/patients')
def list_patients():
    logging.debug('Accès à la liste des patients')
    patients = Patient.query.all()
    for patient in patients:
        # Convertir la date de naissance en utilisant la fonction personnalisée
        patient.date_of_birth = convert_date_of_birth(patient.date_of_birth)
    return render_template('patients.html', patients=patients)

# Route pour afficher la liste des professionnels de santé
@app.route('/health_professionals')
def list_health_professionals():
    logging.debug('Accès à la liste des professionnels de santé')
    # Ajoutez ici la logique pour récupérer la liste des professionnels de santé depuis la base de données
    return render_template('health_professionals.html')

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Rendez-vous supprimé avec succès'}), 200
    else:
        return jsonify({'error': 'Rendez-vous non trouvé'}), 404

@app.route('/')
def index():
    logging.debug('Accès à la page d\'accueil')
    # Récupérer tous les rendez-vous triés par date du rendez-vous
    appointments = Appointment.query.order_by(Appointment.appointment_time).all()
    # Convertir la date de naissance pour chaque patient associé à un rendez-vous
    for appointment in appointments:
        if appointment.patient:  # Vérifier si le rendez-vous a un patient associé
            if appointment.patient.date_of_birth:  # Vérifier si la date de naissance n'est pas vide
                appointment.patient.date_of_birth = convert_date_of_birth(appointment.patient.date_of_birth)
    # Récupérer le nombre total de rendez-vous
    total_appointments = len(appointments)
    # Rendre le modèle HTML avec la liste des rendez-vous et le nombre total de rendez-vous
    return render_template('index.html', appointments=appointments, total_appointments=total_appointments)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
