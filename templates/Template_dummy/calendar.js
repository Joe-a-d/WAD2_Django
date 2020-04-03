$(function() {

    $('#calendar').fullCalendar({
      themeSystem: 'bootstrap4',
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,agendaWeek,agendaDay,listMonth'
      },
      weekNumbers: true,
      eventLimit: true, 
      events: 'https://fullcalendar.io/demo-events.json'
    });
  
  });