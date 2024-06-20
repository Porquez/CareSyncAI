$(document).ready(function() {
    $('#calendar').fullCalendar({
        locale: 'fr',
        events: '/appointments',
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        eventClick: function(event) {
            if (event.url) {
                window.open(event.url);
                return false;
            }
        }
    });
});
