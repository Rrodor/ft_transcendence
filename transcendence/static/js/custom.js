document.addEventListener('DOMContentLoaded', function () {
    var alertContainer = document.getElementById('alert-container');
	var errorAlerts = document.querySelectorAll('.alert-error');
    if (alertContainer) {
        var alerts = alertContainer.getElementsByClassName('alert');
        for (var i = 0; i < alerts.length; i++) {
            alerts[i].addEventListener('closed.bs.alert', function () {
                document.getElementById('main-navbar').classList.remove('d-none');
            });
        }
    }
	errorAlerts.forEach(function(alert) {
        alert.classList.remove('alert-error');
        alert.classList.add('alert-danger');
    });
});