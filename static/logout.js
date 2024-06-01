document.addEventListener('DOMContentLoaded', function() {
    // Ajouter un écouteur d'événements au bouton de déconnexion
    document.getElementById('logoutButton').addEventListener('click', function() {
        // Appeler l'API /logout pour effectuer la déconnexion
        fetch('/logout', {
            method: 'POST' // ou 'GET' selon la méthode utilisée par votre API
        })
        .then(response => {
            if (response.ok) {
                // Rediriger l'utilisateur vers la page de connexion
                window.location.href = '/login'; // Remplacez '/login' par l'URL de votre page de connexion
            } else {
                console.error('Erreur lors de la déconnexion');
            }
        })
        .catch(error => console.error('Erreur réseau :', error));
    });
});
