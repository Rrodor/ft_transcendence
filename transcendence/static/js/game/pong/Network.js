export function sendBallPositionToServer(position)
{
	fetch('http://127.0.0.1:8000/pong/update_ball_position', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ position }),
	})
	.then(response => response.json())
	.then(data => console.log(data))
	.catch((error) => {
		console.error('Error:', error);
	});
}

export function sendScorePlayerLeft(score)
{
	fetch('http://127.0.0.1:8000/pong/send_score_player_left', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ score }),
	})
	.then(response => response.json())
	.then(data => console.log(data))
	.catch((error) => {
		console.error('Error:', error);
	});
}

export function sendScorePlayerRight(score)
{
	fetch('http://127.0.0.1:8000/pong/send_score_player_right', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ score }),
	})
	.then(response => response.json())
	.then(data => console.log(data))
	.catch((error) => {
		console.error('Error:', error);
	});
}

export function sendScoreAI(score)
{
	fetch('http://127.0.0.1:8000/pong/send_score_ai', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ score }),
	})
	.then(response => response.json())
	.then(data => console.log(data))
	.catch((error) => {
		console.error('Error:', error);
	});
}
