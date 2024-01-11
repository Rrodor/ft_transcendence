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
	var legendHtml = myChart1.data.labels.map(function(label, index) {
        var color = myChart1.data.datasets[0].backgroundColor[index];
        return '<span style="display:inline-block;margin-right:10px;">' +
               '<span style="background:' + color + ';width:12px;height:12px;display:inline-block;margin-right:5px;"></span>' +
               '<span>' + label + '</span>' +
               '</span>';
    }).join("");

    document.getElementById('myChartLegend').innerHTML = legendHtml;
});
