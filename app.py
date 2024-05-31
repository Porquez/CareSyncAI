import os
import logging
import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

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

# Clé secrète pour la signature des t
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# Initialisez la base de données
db = SQLAlchemy(app)

# Initialisez l'extension Flask-JWT-Extended
jwt = JWTManager(app)

# Configuration de la journalisation
logging.basicConfig(level=logging.DEBUG)  # Définir le niveau de journalisation sur DEBUG

# Modèle de base de données pour stocker les informations d'identification des utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Champ pour stocker le rôle de l'utilisateur
    id_patient = db.Column(db.Integer)

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
    status = db.Column(db.String(50))  # Ajouter une colonne pour le statut du rendez-vous
    health_professional = db.relationship('HealthProfessional', backref=db.backref('appointments', lazy=True))

# La route /login gère la vérification des informations d'identification de l'utilisateur et génère un token JWT valide en cas de succès.
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Recherche de l'utilisateur dans la base de données
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Récupération de l'ID du patient associé à cet utilisateur
            patient_id = user.id_patient
            # Création du token d'accès avec l'identité de l'utilisateur et l'ID du patient comme réclamations
            access_token = create_access_token(identity=username, user_claims={'patient_id': patient_id})
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'error': 'Identifiants invalides'}), 401
    else:
        return jsonify({'error': 'Méthode non autorisée'}), 405

# La route /protected est un exemple de route protégée qui nécessite un token JWT valide pour y accéder. La décoration @jwt_required() assure que seuls les utilisateurs authentifiés peuvent accéder à cette route.
@app.route('/protected', methods=['GET'])
#@jwt_required()
def protected():
    current_user = get_jwt_identity()
    patient_id = get_jwt_claims().get('patient_id')
    return jsonify(logged_in_as=current_user, patient_id=patient_id), 200

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
            return converted_date
        except ValueError as e:
            try:
                # Si la conversion échoue, essayez un autre format
                date_obj = datetime.strptime(date_string, '%d-%m-%Y')
                converted_date = date_obj.strftime('%d-%m-%Y')  # Format en 'DD-MM-YYYY'
                return converted_date
            except ValueError as e:
                logging.error(f"Erreur lors de la conversion de {date_string} : {e}")
                # Si les deux conversions échouent, renvoyez None ou une valeur par défaut
                return None
    else:
        logging.error("La chaîne de date de naissance est vide.")
        return None

# Route pour ajouter un patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        try:
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
            # Créer une nouvelle instance de Patient
            new_patient = Patient(name=name, first_name=first_name, date_of_birth=date_of_birth, sex=sex, prefix=prefix,
                                    place_of_birth=place_of_birth, social_security_number=social_security_number,
                                    medical_history=medical_history, medications=medications,
                                    allergies=allergies, emergency_contacts=emergency_contacts)

            # Ajouter le patient à la base de données
            db.session.add(new_patient)
            db.session.commit()
    
            #Exemple de réponse JSON
            return jsonify({'message': 'Patient ajouté avec succès'}), 201
        except Exception as e:
            # En cas d'erreur, annuler les modifications et enregistrer l'erreur dans les logs
            db.session.rollback()
            logging.error(f"Erreur lors de l'ajout du patient : {e}")
            return jsonify({'error': 'Erreur lors de l\'ajout du patient'}), 500
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

@app.route('/update-appointment-status/<int:appointment_id>', methods=['PATCH'])
def update_appointment_status(appointment_id):
    try:
        # Récupérer le rendez-vous à partir de l'ID
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            # Récupérer le nouveau statut à partir des données de la requête PATCH
            new_status = request.json.get('status')
            if new_status:
                # Mettre à jour le statut du rendez-vous
                appointment.status = new_status
                db.session.commit()
                return jsonify({'message': 'Statut du rendez-vous mis à jour avec succès'}), 200
            else:
                return jsonify({'error': 'Le nouveau statut est manquant dans la requête'}), 400
        else:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404
    except Exception as e:
        # En cas d'erreur, annuler les modifications et enregistrer l'erreur dans les logs
        db.session.rollback()
        logging.error(f"Erreur lors de la mise à jour du statut du rendez-vous : {e}")
        return jsonify({'error': 'Erreur lors de la mise à jour du statut du rendez-vous'}), 500

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        # Récupérer l'utilisateur authentifié à partir du token JWT
        current_user = get_jwt_identity()
        
        # implementer la logicie de suppresion ou pas par le professionnel de santé peutqui  supprimer uniquement les rendez-vous qu'il a créés
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            # Vérifier si le rendez-vous peut être supprimé en fonction du délai configuré
            suppression_delai_heures = config.get('suppression_delai_heures', 24)
            delai_suppression = timedelta(hours=suppression_delai_heures)
            heure_actuelle = datetime.now()
            heure_rendez_vous = appointment.appointment_time

            if heure_actuelle - heure_rendez_vous > delai_suppression:
                # Si le délai est écoulé, renvoyer un message d'erreur
                return jsonify({'error': f'Impossible de supprimer le rendez-vous. Le délai de suppression est écoulé.'}), 403
            else:
                # Supprimer le rendez-vous de la base de données
                db.session.delete(appointment)
                db.session.commit()
                return jsonify({'message': 'Rendez-vous supprimé avec succès'}), 200
        else:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404
    except Exception as e:
        # En cas d'erreur, annuler les modifications et enregistrer l'erreur dans les logs
        db.session.rollback()
        logging.error(f"Erreur lors de la suppression du rendez-vous : {e}")
        return jsonify({'error': 'Erreur lors de la suppression du rendez-vous'}), 500
  
# Route pour la page d'accueil
@app.route('/')
#@jwt_required()  # Cette décoration nécessite un token JWT valide pour accéder à la route
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

# Route pour les rendez-vous à venir pour un patient spécifique
@app.route('/upcoming-appointments/<int:patient_id>')
#@jwt_required()  # Cette décoration nécessite un token JWT valide pour accéder à la route
def upcoming_appointments(patient_id):
    logging.debug(f'Accès aux rendez-vous à venir pour le patient {patient_id}')
    
    # Récupérer tous les rendez-vous à venir pour le patient spécifié, triés par date du rendez-vous
    appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.appointment_time).all()
    logging.debug(f'Nombre total de rendez-vous à venir pour le patient {patient_id} : {len(appointments)}')
    
    # Convertir la date de naissance pour chaque patient associé à un rendez-vous
    for appointment in appointments:
        if appointment.patient and appointment.patient.date_of_birth:
            appointment.patient.date_of_birth = convert_date_of_birth(appointment.patient.date_of_birth)
    
    # Convertir le nom complet du professionnel de santé
    for appointment in appointments:
        if appointment.health_professional:
            appointment.health_professional_name = f"{appointment.health_professional.first_name} {appointment.health_professional.last_name}"
    
    # Créer une liste JSON des rendez-vous à venir
    upcoming_appointments = []
    for appointment in appointments:
        upcoming_appointments.append({
            'id': appointment.id,
            'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'patient_name': f"{appointment.patient.prefix} {appointment.patient.name} {appointment.patient.first_name}",
            'health_professional_name': appointment.health_professional_name,
            'status': appointment.status
        })
    
    return jsonify(upcoming_appointments)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Choix de l'URL et du port en fonction de l'existence de l'URL HTTPS
    if https_url:
        app.run(debug=True, host=https_url, port=port, ssl_context='adhoc')
    else:
        app.run(debug=True, host=http_url, port=port)
