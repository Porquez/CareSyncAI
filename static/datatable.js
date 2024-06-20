$(document).ready(function() {
    $('#appointmentTable').DataTable({
        paging: true,
        pageLength: 50,
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
        },
        ordering: false,
        lengthMenu: [50, 100, 500],
        initComplete: function() {
            $('#appointmentTable').show();
        }
    });
});
