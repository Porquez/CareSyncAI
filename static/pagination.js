document.addEventListener("DOMContentLoaded", function() {
    // Fonction pour mettre à jour les informations de pagination
    function updatePageInfo(startIndex, endIndex, totalItems) {
        document.getElementById('page-info').innerText = `${startIndex} - ${endIndex} sur ${totalItems}`;
    }

    // Fonction pour afficher les éléments par page
    function displayItemsPerPage(itemsPerPage, currentPage, totalItems) {
        const startIndex = (currentPage - 1) * itemsPerPage + 1;
        const endIndex = Math.min(currentPage * itemsPerPage, totalItems);
        updatePageInfo(startIndex, endIndex, totalItems);
    }

    function deleteAppointment(appointmentId) {
        const confirmed = confirm("Voulez-vous vraiment supprimer ce rendez-vous ?");
        if (confirmed) {
            // Envoyer une requête AJAX pour supprimer le rendez-vous
            fetch(`/appointments/${appointmentId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(response => {
                if (response.ok) {
                    // Actualiser la page après la suppression
                    location.reload();
                } else {
                    // Gérer les erreurs de suppression
                    console.error('Erreur lors de la suppression du rendez-vous');
                }
            })
            .catch(error => console.error('Erreur lors de la suppression du rendez-vous : ', error));
        }
    }
    
    // Initialisation
    let currentPage = 1;
    let itemsPerPage = 50; // Valeur par défaut
    const totalItems = totalAppointments; // Utilisez la variable JavaScript définie dans index.html
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const itemsPerPageSelect = document.getElementById('items-per-page');

    // Afficher les éléments par page lors de la sélection
    itemsPerPageSelect.addEventListener('change', function() {
        itemsPerPage = parseInt(this.value);
        currentPage = 1; // Revenir à la première page
        displayItemsPerPage(itemsPerPage, currentPage, totalItems);
    });

    // Navigation vers la page précédente
    prevButton.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            displayItemsPerPage(itemsPerPage, currentPage, totalItems);
        }
    });

    // Navigation vers la page suivante
    nextButton.addEventListener('click', function() {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            displayItemsPerPage(itemsPerPage, currentPage, totalItems);
        }
    });

    // Afficher les éléments par page au chargement initial
    displayItemsPerPage(itemsPerPage, currentPage, totalItems);
});
