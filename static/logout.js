document.addEventListener('DOMContentLoaded', function() {
    // Ajouter un �couteur d'�v�nements au bouton de d�connexion
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            // Appeler l'API /logout pour effectuer la d�connexion
            fetch('/logout', {
                method: 'POST' // ou 'GET' selon la m�thode utilis�e par votre API
            })
            .then(response => {
                if (response.ok) {
                    // Rediriger l'utilisateur vers la page de connexion
                    window.location.href = '/login'; // Remplacez '/login' par l'URL de votre page de connexion
                } else {
                    console.error('Erreur lors de la d�connexion');
                }
            })
            .catch(error => console.error('Erreur r�seau :', error));
        });
    } else {
        console.error('Le bouton de d�connexion n\'a pas �t� trouv�.');
    }
});

// Fonction alternative pour la d�connexion, appel�e depuis un autre script
function logout() {
    // Appeler l'API /logout pour effectuer la d�connexion
    fetch('/logout', {
        method: 'POST' // ou 'GET' selon la m�thode utilis�e par votre API
    })
    .then(response => {
        if (response.ok) {
            // Rediriger l'utilisateur vers la page de connexion
            window.location.href = '/login'; // Remplacez '/login' par l'URL de votre page de connexion
        } else {
            console.error('Erreur lors de la d�connexion');
        }
    })
    .catch(error => console.error('Erreur r�seau :', error));
}
