// Fonction de filtrage générique
function filterTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = event.target;
    filter = input.value.toUpperCase();
    table = document.getElementById("appointmentTable");
    tr = table.getElementsByTagName("tr");
    var columnIndex = parseInt(input.dataset.column); // Numéro de colonne
    var columnType = input.dataset.type; // Type de colonne

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[columnIndex];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (columnType === "text") {
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            } else if (columnType === "date") {
                // Filtrage de la colonne de date
                if (filterDate(txtValue, filter)) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}

// Fonction pour filtrer les dates dans un format spécifique
function filterDate(dateString, filterString) {
    // Parse the date string based on the expected format
    var dateParts = dateString.split('-'); // Split by dash

    // Extract date components
    var year = parseInt(dateParts[2]);
    var month = parseInt(dateParts[1]);
    var day = parseInt(dateParts[0]);

    // Parse the filter string to extract filter components
    var filterParts = filterString.split('-'); // Split by dash

    // Compare each date component with filter component
    for (var i = 0; i < filterParts.length; i++) {
        var filterValue = parseInt(filterParts[i]);
        if (isNaN(filterValue)) continue; // Skip non-numeric filter components

        if (i === 0 && year !== filterValue) return false; // Year mismatch
        if (i === 1 && month !== filterValue) return false; // Month mismatch
        if (i === 2 && day !== filterValue) return false; // Day mismatch
    }

    return true; // All components match
}
// Appeler la fonction de filtrage lors de la saisie dans les champs de recherche
document.getElementById("Filtre_health_professional_name").addEventListener("input", filterTable);
document.getElementById("Filtre_name").addEventListener("input", filterTable);
