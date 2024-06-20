// Sélectionner toutes les cellules de date
const dateCells = document.querySelectorAll('.appointment-date');

// Parcourir chaque cellule de date
dateCells.forEach(cell => {
    // Ajouter un gestionnaire d'événements pour le survol de la souris
    cell.addEventListener('mouseenter', function(event) {
        // Récupérer la date associée à cette cellule
        const date = cell.dataset.date;
        
        // Afficher la bulle d'information avec le libellé correspondant
        const formattedDate = moment(date, 'DD-MM-YYYY').locale('fr').format('dddd DD MMMM YYYY');
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = formattedDate;
        
        // Positionner la bulle d'information à côté de la cellule
        const rect = cell.getBoundingClientRect();
        tooltip.style.top = rect.top + 'px';
        tooltip.style.left = rect.right + 'px';
        
        // Ajouter la bulle d'information au corps du document
        document.body.appendChild(tooltip);
    });

    // Ajouter un gestionnaire d'événements pour la sortie de la souris
    cell.addEventListener('mouseleave', function(event) {
        // Supprimer la bulle d'information lorsque la souris quitte la cellule
        const tooltip = document.querySelector('.tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    });
});