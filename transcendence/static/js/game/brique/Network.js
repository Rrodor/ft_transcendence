export function sendScore(score, userId) {
	fetch('/brique/sendscore/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ score: score, userId: userId }),
	})
	.then(response => response.json())
	.then(data => console.log(data))
	.catch((error) => {
		console.error('Error:', error);
	});
}