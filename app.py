import os
import logging
import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)

# Lecture du fichier de configuration JSON
config_path = os.path.join(os.getcwd(), 'conf', 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

# Utilisation des valeurs du fichier de configuration
app_dir = config.get('app_dir')
db_filename = config.get('db_filename')
http_url = config.get('http_url')
https_url = config.get('https_url')
port = config.get('port')

# Chemin complet vers le répertoire contenant le fichier de base de données
db_path = os.path.join(app_dir, db_filename)

# Configuration de l'URI de base de données avec le chemin complet
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Initialisez la base de données
db = SQLAlchemy(app)

# Configuration de la journalisation
logging.basicConfig(level=logging.DEBUG)  # Définir le niveau de journalisation sur DEBUG

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    prefix = db.Column(db.String(10))
    place_of_birth = db.Column(db.String(100))
    social_security_number = db.Column(db.String(15))
    medical_history = db.Column(db.String(100))
    medications = db.Column(db.String(100))
    emergency_contacts= db.Column(db.String(100))
    allergies = db.Column(db.String(100))

class Caregiver(db.Model):
    __tablename__ = 'caregivers'
    id = db.Column(db.Integer, primary_key=True)


class HealthProfessional(db.Model):
    __tablename__ = 'health_professionals'
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(50)) 
    first_name = db.Column(db.String(50)) 
    last_name = db.Column(db.String(50)) 
    rpps = db.Column(db.Integer) 
    name = db.Column(db.String(50)) 
    specialty = db.Column(db.String(50))

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregivers.id'))
    caregiver = db.relationship('Caregiver', backref=db.backref('appointments', lazy=True))
    health_professional_id = db.Column(db.Integer, db.ForeignKey('health_professionals.id'))
    health_professional = db.relationship('HealthProfessional', backref=db.backref('appointments', lazy=True))

# Route pour afficher la liste des rendez-vous des patients
@app.route('/appointments')
def list_appointments():
    logging.debug('Accès à la liste des rendez-vous des patients')
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

def convert_date_of_birth(date_string):
    if date_string:
        try:
            # Utiliser strptime pour convertir la chaîne en objet datetime
            date_obj = datetime.strptime(date_string, '%Y-%m-%d')
            converted_date = date_obj.strftime('%d-%m-%Y')  # Format en 'DD-MM-YYYY'
            print(f"Conversion réussie : {date_string} -> {converted_date}")
            return converted_date
        except ValueError as e:
            print(f"Erreur lors de la conversion de {date_string} : {e}")
            try:
                # Si la conversion échoue, essayez un autre format
                date_obj = datetime.strptime(date_string, '%d-%m-%Y')
                converted_date = date_obj.strftime('%d-%m-%Y')  # Format en 'DD-MM-YYYY'
                print(f"Conversion réussie : {date_string} -> {converted_date}")
                return converted_date
            except ValueError as e:
                print(f"Erreur lors de la conversion de {date_string} : {e}")
                # Si les deux conversions échouent, renvoyez None ou une valeur par défaut
                return None
    else:
        print("La chaîne de date de naissance est vide.")
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
        # Vérifier si le rendez-vous peut être supprimé en fonction du délai configuré
        suppression_delai_heures = config.get('suppression_delai_heures', 24)
        delai_suppression = timedelta(hours=suppression_delai_heures)
        heure_actuelle = datetime.now()
        heure_rendez_vous = appointment.appointment_time

        if heure_rendez_vous - heure_actuelle > delai_suppression:
            # Si le délai n'est pas écoulé, renvoyer un message d'erreur
            return jsonify({'error': f'Impossible de supprimer le rendez-vous. Le délai de suppression est de {suppression_delai_heures} heures.'}), 403
        else:
            # Supprimer le rendez-vous de la base de données
            db.session.delete(appointment)
            db.session.commit()
            return jsonify({'message': 'Rendez-vous supprimé avec succès'}), 200
    else:
        return jsonify({'error': 'Rendez-vous non trouvé'}), 404

# Route pour la page d'accueil
@app.route('/')
def index():
    logging.debug('Accès à la page d\'accueil')
    # Récupérer tous les rendez-vous triés par date du rendez-vous
    appointments = Appointment.query.order_by(Appointment.appointment_time).all()
    logging.debug(f'Nombre total de rendez-vous récupérés : {len(appointments)}')
    
    # Convertir la date de naissance pour chaque patient associé à un rendez-vous
    for appointment in appointments:
        if appointment.patient:  # Vérifier si le rendez-vous a un patient associé
            if appointment.patient.date_of_birth:  # Vérifier si la date de naissance n'est pas vide
                appointment.patient.date_of_birth = convert_date_of_birth(appointment.patient.date_of_birth)
        
    # Convertir le nom complet du professionnel de santé
    for appointment in appointments:
        if appointment.health_professional:  # Vérifier si le rendez-vous a un professionnel de santé associé
            # Concaténer les champs first_name et last_name pour former le nom complet du professionnel de santé
            appointment.health_professional_name = f"{appointment.health_professional.first_name} {appointment.health_professional.last_name}"
    logging.debug('Noms des professionnels de santé récupérés et concaténés avec succès')
    
    # Récupérer le nombre total de rendez-vous
    total_appointments = len(appointments)
    logging.debug(f'Nombre total de rendez-vous après conversion des noms : {total_appointments}')
    
    # Récupérer la date actuelle
    now = datetime.now()
    logging.debug(f'Date actuelle : {now}')
    
    # Récupérer les noms et prénoms uniques des médecins associés aux rendez-vous
    health_professionals = [appointment.health_professional for appointment in appointments if appointment.health_professional]
    logging.debug(f'Noms des professionnels de santé récupérés : {health_professionals}')
    
    # Récupérer le nom et le prénom du premier médecin (par exemple)
    if health_professionals:
        health_professional = health_professionals[0]
        health_professional_name = f"{health_professional.first_name} {health_professional.last_name}"
        logging.debug(f'Nom complet du premier professionnel de santé : {health_professional_name}')
    else:
        health_professional_name = None
    
    # Rendre le modèle HTML avec la liste des rendez-vous, le nom du médecin et le nombre total de rendez-vous
    return render_template('index.html', appointments=appointments, total_appointments=total_appointments, now=now, health_professional_name=health_professional_name)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Choix de l'URL et du port en fonction de l'existence de l'URL HTTPS
    if https_url:
        app.run(debug=True, host=https_url, port=port, ssl_context='adhoc')
    else:
        app.run(debug=True, host=http_url, port=port)
