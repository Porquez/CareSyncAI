document.addEventListener('DOMContentLoaded', function() {
    // Ajouter un �couteur d'�v�nements au bouton de d�connexion
    document.getElementById('logoutButton').addEventListener('click', function() {
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
});
