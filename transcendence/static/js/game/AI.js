let elapsedTime = 1;
let	paddlePos = 0;
let ballPos = [];

export function AImove(trueBallPos, truePaddlePos, paddleSpeed, deltaTime)
{
	elapsedTime += deltaTime;
	let ballFinalPos = 0;

	if (elapsedTime >= 1)
	{
		console.log("one sec");
		elapsedTime = 0;
		console.log("trueBallPos.z = " + trueBallPos.position.z);
		ballPos.push(trueBallPos.clone());
		if (ballPos.length == 3)
			ballPos.shift();
		paddlePos = truePaddlePos;
	}
	if (ballPos.lenght == 1)
	{
		console.log("Alpha ballPos.z = " + ballPos[0].position.z);
		if (ballPos[0].position.z > paddlePos && paddlePos < 8.75)
		{
			paddlePos += paddleSpeed * deltaTime;
		}
		if (ballPos[0].position.z < paddlePos && paddlePos > -8.75)
		{
			paddlePos -= paddleSpeed * deltaTime;
		}
	}
	else if (ballPos.length == 2)
	{
		console.log("Omega ballPos.z = " + ballPos[1].position.z);
		if (ballDirectionIsLeft())
		{
			if (ballPos[1].position.z > paddlePos && paddlePos < 8.75)
			{
				paddlePos += paddleSpeed * deltaTime;
			}
			if (ballPos[1].position.z < paddlePos && paddlePos > -8.75)
			{
				paddlePos -= paddleSpeed * deltaTime;
			}
		}
		else
		{
			ballFinalPos = ballCollision();
			console.log("ballFinalPos = " + ballFinalPos);
			if (ballFinalPos > paddlePos && paddlePos < 8.75 && ballFinalPos > -10)
			{
				paddlePos += paddleSpeed * deltaTime;
			}
			if (ballFinalPos < paddlePos && paddlePos > -8.75 && ballFinalPos < 10)
			{
				paddlePos -= paddleSpeed * deltaTime;
			}
		}

	}
	return paddlePos;
}

function ballDirectionIsLeft()
{
	if (ballPos[0].position.x > ballPos[1].position.x)
	{
		console.log("going to the left");
		return true;
	}
	else if (ballPos[0].position.x < ballPos[1].position.x)
	{
		console.log("going to the right");
		return false;
	}
	return false;
}

function ballCollision()
{
	let A = 0;
	let B = 0;
	A = (ballPos[1].position.z - ballPos[0].position.z) / (ballPos[1].position.x - ballPos[0].position.x);
	B = ballPos[0].position.z - A * ballPos[0].position.x;
	console.log("A = " + A);
	console.log("B = " + B);

	return (A * 10 + B);
}
