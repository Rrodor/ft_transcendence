
/*
	function checkGoal()
	{
		// Check if the ball is 2 units behind the left paddle on x axis
		if (ball.position.x < paddleLeft.position.x - 2)
		{
			// If the ball is behind the left paddle, increment the score of the right player
			scoreRight++;
			updateScoreSprite(scoreRightSprite, scoreRight);

			// Reset the ball
			ball.position.set(0, 0, 0);
			ball.rotation.y = Math.random() * Math.PI * 2;
			const forward = new THREE.Vector3(0, 0, -1);
			forward.applyQuaternion(ball.quaternion);
			const speed = 0.1;
			const velocity = forward.multiplyScalar(speed);
			ballVelocity = velocity;
		}
		if (ball.position.x > paddleRight.position.x + 2)
		{
			// If the ball is behind the right paddle, increment the score of the left player
			scoreLeft++;
			updateScoreSprite(scoreLeftSprite, scoreLeft);

			// Reset the ball
			ball.position.set(0, 0, 0);
			ball.rotation.y = Math.random() * Math.PI * 2;
			const forward = new THREE.Vector3(0, 0, -1);
			forward.applyQuaternion(ball.quaternion);
			const speed = 0.1;
			const velocity = forward.multiplyScalar(speed);
			ballVelocity = velocity;
		}
	}

*/
