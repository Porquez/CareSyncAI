DROP TABLE appointments;
DROP TABLE patients;
DROP TABLE health_professionals;
DROP TABLE user;

CREATE TABLE user (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT);
CREATE TABLE patients (id INTEGER PRIMARY KEY, name TEXT, first_name TEXT, date_of_birth TEXT, sex TEXT, prefix TEXT, place_of_birth TEXT, social_security_number TEXT, medical_history TEXT, medications TEXT, allergies TEXT, emergency_contacts TEXT);
CREATE TABLE appointments (id INTEGER PRIMARY KEY, caregiver_id INTEGER, health_professional_id INTEGER, patient_id INTEGER,  appointment_time TEXT, duration TEXT, confirmed BOOLEAN);
CREATE TABLE health_professionals (id INTEGER PRIMARY KEY AUTOINCREMENT, prefix TEXT, first_name TEXT, last_name TEXT, rpps INTEGER UNIQUE, name TEXT, specialty TEXT);

INSERT INTO patients values (1,'Patient 1','Prenom','1969-12-20','M.','','Amiens','1691180','','','','');
INSERT INTO patients values (2,'Patient 2','Prenom','1980-11-01','Mme','','Amiens','1601080','','','','');

INSERT INTO appointments values (1,1,1,1,'2024-06-18 15:00:00','1400.0','0');
INSERT INTO appointments values (2,1,1,1,'2024-07-17 15:00:00','1400.0','0');
INSERT INTO appointments values (3,1,1,1,'2024-07-17 15:00:00','1400.0','0');
INSERT INTO appointments values (4,1,2,2,'2024-08-17 09:00:00','1400.0','0');
INSERT INTO appointments values (5,1,2,2,'2024-09-18 10:00:00','1400.0','0');

INSERT INTO appointments values (6,1,1,1,'2025-06-18 15:00:00','1400.0','0');
INSERT INTO appointments values (7,1,1,1,'2025-07-17 15:00:00','1400.0','0');
INSERT INTO appointments values (8,1,1,1,'2025-07-17 15:00:00','1400.0','0');
INSERT INTO appointments values (9,1,2,2,'2025-08-17 09:00:00','1400.0','0');
INSERT INTO appointments values (10,1,2,2,'2025-09-18 10:00:00','1400.0','0');

INSERT INTO appointments values (11,1,1,1,'2026-06-18 15:00:00','1400.0','0');
INSERT INTO appointments values (12,1,1,1,'2026-07-17 15:00:00','1400.0','0');
INSERT INTO appointments values (13,1,1,1,'2026-07-17 15:00:00','1400.0','0');
INSERT INTO appointments values (14,1,2,2,'2026-08-17 09:00:00','1400.0','0');
INSERT INTO appointments values (15,1,2,2,'2026-09-18 10:00:00','1400.0','0');

INSERT INTO health_professionals values (1,'1','Medecin 1','Prenom','122222222','','Medecine');
INSERT INTO health_professionals values (2,'2','Medecin 2','Prenom','123222222','','Medecine');

INSERT INTO user values( 1, 'pporquez','Azerty','Admin');
INSERT INTO user values( 2, 'admin','Azerty','Admin');
INSERT INTO user values( 3, 'ppz','Azerty','Admin');
