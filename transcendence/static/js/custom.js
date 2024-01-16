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
				labels: [labelVictories, labelDefeats],
				datasets: [{
					label: labelPlayerStats,
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

    if (document.getElementById('myChart2')) {
        var ctx2 = document.getElementById('myChart2').getContext('2d');
        
        var myChart2 = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: brickScores.map((_, index) => `Game ${index + 1}`),
                datasets: [{
                    label: labelPoints,
                    data: brickScores,
                    backgroundColor: 'rgb(21, 87, 36)',
                    borderColor: 'rgb(21, 87, 36)',
                    borderWidth: 1
                }]
            },
            options: {
				scales: {
					y: {
						beginAtZero: true
					}
				},
                responsive: true,
                maintainAspectRatio: true
            }
        });
    }
	var currentMatchId;
	var currentOpponentId

	document.querySelectorAll('.play-match-link').forEach(function(link) {
		link.onclick = function(e) {
			e.preventDefault();
			currentMatchId = this.getAttribute('data-match-id');
			currentOpponentId = this.getAttribute('data-opponent-id');
			var passwordModal = new bootstrap.Modal(document.getElementById('passwordModal'));
			passwordModal.show();
		}
	});
	document.getElementById('passwordForm').onsubmit = function(e) {
		e.preventDefault();
		var password = document.getElementById('password').value;
		$.ajax({
			url: '/verify_password/',
			type: 'post',
			data: {
				'password': password,
				'match_id': currentMatchId,
				'opponent_id': currentOpponentId,
				'csrfmiddlewaretoken': '{{ csrf_token }}'
			},
			success: function(response) {
				if (response.success) {
					// Le mot de passe est correct, redirigez vers la page du match
					window.location.href = "/play_match/" + currentMatchId + "/";
				} else {
					// Le mot de passe est incorrect, affichez un message d'erreur
					alert('Incorrect password');
				}
			}
		});
	}
});

function changeLanguage(languageCode) {
    document.getElementById('language-input').value = languageCode;
    document.getElementById('language-form').submit();
}
