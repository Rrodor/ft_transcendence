export function sendBallPositionToServer(position)
{
	fetch('/pong/update_ball_position', {
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

export function sendScore(scoreLeft, scoreRight, userId)
{
	fetch('/pong/sendscore/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ scoreLeft: scoreLeft, scoreRight: scoreRight, userId: userId }),
	})
	.then(response => response.json())
	.then(data => console.log(data))
	.catch((error) => {
		console.error('Error:', error);
	});
}

export function sendScoreAI(score)
{
	fetch('/pong/send_score_ai', {
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
