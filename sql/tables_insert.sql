DROP TABLE appointments;
DROP TABLE patients;
DROP TABLE health_professionals;
DROP TABLE user;

CREATE TABLE user (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, id_patient INTEGER);
CREATE TABLE patients (id INTEGER PRIMARY KEY, name TEXT, first_name TEXT, date_of_birth TEXT, sex TEXT, prefix TEXT, place_of_birth TEXT, social_security_number TEXT, medical_history TEXT, medications TEXT, allergies TEXT, emergency_contacts TEXR, tel TEXT);
CREATE TABLE appointments (id INTEGER PRIMARY KEY, caregiver_id INTEGER, health_professional_id INTEGER, patient_id INTEGER,  appointment_time TEXT, duration TEXT, confirmed BOOLEAN, status TEXT );
CREATE TABLE health_professionals (id INTEGER PRIMARY KEY AUTOINCREMENT, prefix TEXT, first_name TEXT, last_name TEXT, rpps INTEGER UNIQUE, name TEXT, specialty TEXT);

INSERT INTO patients values (1,'Patient 1','Prenom','1969-12-20','Masculin','M.','Amiens','1691180','','','','','06.50.45.31.76');
INSERT INTO patients values (2,'Patient 2','Prenom','1980-11-01','Féminin','Mme','Amiens','1601080','','','','','07.12.45.31.76');
INSERT INTO patients values (3,'Patient 3','Prenom','1969-12-20','Masculin','M.','Amiens','1691180','','','','','03.22.33.66.37');
INSERT INTO patients values (4,'Patient 4','Prenom','1980-11-01','Féminin','Mme','Amiens','1601080','','','','','');
INSERT INTO patients values (5,'Patient 5','Prenom','1967-12-20','Masculin','M.','Amiens','1691180','','','','','');
INSERT INTO patients values (6,'Patient 6','Prenom','1981-11-01','Féminin','Mme','Amiens','1601080','','','','','');


INSERT INTO appointments values (1,1,1,1,'2024-06-18 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (2,1,1,1,'2024-07-17 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (3,1,1,1,'2024-07-17 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (4,1,2,2,'2024-08-17 09:00:00','1400.0','0','A venir');
INSERT INTO appointments values (5,1,2,2,'2024-09-18 10:00:00','1400.0','0','A venir');

INSERT INTO appointments values (6,1,1,1,'2025-06-18 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (7,1,1,1,'2025-07-17 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (8,1,1,1,'2025-07-17 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (9,1,2,2,'2025-08-17 09:00:00','1400.0','0','A venir');
INSERT INTO appointments values (10,1,2,2,'2025-09-18 10:00:00','1400.0','0','A venir');

INSERT INTO appointments values (11,1,1,1,'2026-06-18 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (12,1,1,1,'2026-07-17 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (13,1,1,1,'2026-07-17 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (14,1,2,2,'2026-08-17 09:00:00','1400.0','0','A venir');
INSERT INTO appointments values (15,1,2,2,'2026-09-18 10:00:00','1400.0','0','A venir');

INSERT INTO appointments values (16,1,3,1,'2027-06-18 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (17,1,3,1,'2027-07-17 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (18,1,3,1,'2027-07-17 15:00:00','1400.0','0','A venir');
INSERT INTO appointments values (19,1,3,2,'2027-08-17 09:00:00','1400.0','0','A venir');
INSERT INTO appointments values (20,1,3,2,'2027-09-18 10:00:00','1400.0','0','A venir');

INSERT INTO health_professionals values (1,'1','Medecin 1','Prenom','122222222','','Medecine');
INSERT INTO health_professionals values (2,'2','Medecin 2','Prenom','123222222','','Medecine');
INSERT INTO health_professionals values (3,'3','Medecin 3','Prenom','123222223','','Medecine');
INSERT INTO health_professionals values (4,'4','Medecin 4','Prenom','123222224','','Medecine');

INSERT INTO user values( 1, 'pporquez','Azerty','Admin',1);
INSERT INTO user values( 2, 'admin','Azerty','Admin',1);
INSERT INTO user values( 3, 'ppz','Azerty','Admin',1);
