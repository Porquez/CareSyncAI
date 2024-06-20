// Contenu de management.js

// Fonction générique pour gérer les actions sur un rendez-vous
function manageAppointment(action, appointmentId, options = {}) {
    let url = '';
    let method = 'POST';
    let body = {};

    switch (action) {
        case 'changeStatus':
            url = `/update-appointment-status/${appointmentId}`;
            body = { status: options.newStatus };
            method = 'PATCH';
            break;
        case 'confirmAppointment':
            url = `/update-appointment-status/${appointmentId}`;
            body = { status: 'Confirmed' };
            method = 'PATCH';
            break;
        case 'deleteAppointment':
            url = `/appointments/${appointmentId}`;
            method = 'DELETE';
            break;
        case 'moveAppointment':
            url = `/move-appointment/${appointmentId}`;
            body = { newPlanning: options.newPlanning };
            method = 'PATCH';
            break;
        case 'createAppointment':
            url = '/create-appointments';
            body = {
                newPlanning: options.newPlanning,
                patientId: options.patientId,
                healthProfessionalId: options.healthProfessionalId
            };
            method = 'POST';
            break;
        default:
            console.error('Action non reconnue');
            return;
    }

    // Effectuer la requête AJAX appropriée
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
    .then(response => {
        if (response.ok) {
            window.location.reload(); // Recharger la page aprés l'opération réussie
        } else {
            console.error(`Erreur lors de l'action ${action}`);
        }
    })
    .catch(error => console.error('Erreur réseau :', error));
}

// Exemple d'utilisation pour changer le statut d'un rendez-vous
function changeStatus(appointmentId, newStatus) {
    manageAppointment('changeStatus', appointmentId, { newStatus: newStatus });
}

// Exemple d'utilisation pour confirmer un rendez-vous
function confirmAppointment(appointmentId) {
    manageAppointment('confirmAppointment', appointmentId);
}

function deleteAppointment(appointmentId) {
    if (confirm(`Confirmez-vous la suppression du rendez-vous avec l'ID ${appointmentId} ?`)) {
        // Récupérer le jeton CSRF depuis le formulaire spécifique à l'ID de l'appointment
        const csrfToken = document.querySelector(`#deleteForm_${appointmentId} input[name="csrf_token"]`).value;
        const url = `/appointments/${appointmentId}`;
        const method = 'DELETE';
        
        // Récupérer le token JWT depuis la session Flask
        const jwtToken = getJwtTokenFromSession();

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'Authorization': `Bearer ${jwtToken}` // Inclure le JWT dans les en-têtes
            },
        })
        .then(response => {
            if (response.ok) {
                window.location.reload(); // Recharger la page après la suppression réussie
            } else {
                console.error(`Erreur lors de la suppression du rendez-vous avec l'ID ${appointmentId}`);
            }
        })
        .catch(error => console.error('Erreur réseau :', error));
    }
}

// Fonction pour récupérer le jeton JWT depuis la session Flask
function getJwtTokenFromSession() {
    // Implémentez cette fonction pour récupérer le jeton JWT depuis la session
    // Vous pouvez utiliser une requête AJAX pour récupérer le jeton JWT depuis Flask
    // Ou stocker le jeton JWT dans le localStorage côté client lors de la connexion
    return localStorage.getItem('jwtToken'); // Exemple pour récupérer depuis localStorage
}

// Exemple d'utilisation pour déplacer un rendez-vous
function moveAppointment(appointmentId) {
    const newPlanning = prompt(`Entrez la nouvelle date et heure pour le rendez-vous avec l'ID ${appointmentId} (Format : JJ-MM-AAAA HH:MM):`);
    if (newPlanning && newPlanning.trim() !== '') {
        manageAppointment('moveAppointment', appointmentId, { newPlanning: newPlanning });
    }
}

// Exemple d'utilisation pour créer un nouveau rendez-vous
function createAppointment(patientId, healthProfessionalId) {
    const newPlanning = prompt(`Entrez la date et l'heure pour le nouveau rendez-vous (Format : JJ-MM-AAAA HH:MM):`);
    if (newPlanning && newPlanning.trim() !== '') {
        manageAppointment('createAppointment', null, {
            newPlanning: newPlanning,
            patientId: patientId,
            healthProfessionalId: healthProfessionalId
        });
    }
}