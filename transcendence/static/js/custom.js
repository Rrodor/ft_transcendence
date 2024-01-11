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

    var chartData = document.getElementById('chart-data');
    if (chartData && document.getElementById('myChart1')) {
        var ctx1 = document.getElementById('myChart1').getContext('2d');
        var pongVictories = parseInt(chartData.getAttribute('data-pong-victories'), 10);
        var pongDefeats = parseInt(chartData.getAttribute('data-pong-defeats'), 10);

        var myChart1 = new Chart(ctx1, {
            type: 'doughnut',
			data: {
				labels: ['Victories', 'Defeats'],
				datasets: [{
					label: 'Statistiques du Joueur',
					data: [pongVictories, pongDefeats],
					backgroundColor: ['rgb(21, 87, 36)', 'rgb(205, 32, 44)'],
					borderColor: ['rgb(21, 87, 36)', 'rgb(205, 32, 44)'],
					borderWidth: 1
				}]
			},
			options: {
				responsive: true,
				cutoutPercentage: 40,
				maintainAspectRatio: true
			}
			});
    }

    if (chartData && document.getElementById('myChart2')) {
        var ctx2 = document.getElementById('myChart2').getContext('2d');
        
        var myChart2 = new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Victories', 'Defeats'],
                datasets: [{
                    label: 'Statistiques du Joueur',
                    data: [pongVictories, pongDefeats], // Utilisez les mêmes variables pour myChart2
                    backgroundColor: ['rgb(21, 87, 36)', 'rgb(205, 32, 44)'],
                    borderColor: ['rgb(21, 87, 36)', 'rgb(205, 32, 44)'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                cutoutPercentage: 40,
                maintainAspectRatio: true
            }
        });
    }
});


