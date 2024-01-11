const material = new THREE.LineBasicMaterial( { color: 0xff0000 } );
const material2 = new THREE.LineBasicMaterial( { color: 0x00ff00 } );
const material3 = new THREE.LineBasicMaterial( { color: 0xffffff } );


let elapsedTime = 1;
let dircount = 0;
let	paddlePos = 0;
let ballPos = [];
let ballFinalPos = 0;
let dirright = 0;

export function AImove(trueBallPos, truePaddlePos, paddleSpeed, deltaTime, scene)
{
	elapsedTime += deltaTime;
	let traj = false;

	if (elapsedTime >= 1)
	{
		console.log("one sec");
		elapsedTime = 0;
		//console.log("trueBallPos.z = " + trueBallPos.position.z);
		ballPos.push(trueBallPos.clone());
		if (ballPos.length == 3)
			ballPos.shift();
		paddlePos = truePaddlePos;
		dirright = getDirection();
		if (dirright == 0)
			traj = false;
	}
	if (ballPos.lenght == 1)
	{
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
		if (dirright == 1)
		{
			ballFinalPos = ballCollision(scene);
			if (ballFinalPos > paddlePos && paddlePos < 8.75)
			{
				paddlePos += paddleSpeed * deltaTime;
			}
			if (ballFinalPos < paddlePos && paddlePos > -8.75)
			{
				paddlePos -= paddleSpeed * deltaTime;
			}
		}
	}
	return paddlePos;
}

function getDirection()
{
	if (ballPos.length == 2)
	{
		if (ballPos[0].position.x > ballPos[1].position.x)
		{
			dircount = 0;
			return 0;
		}
		else if (ballPos[0].position.x < ballPos[1].position.x && dircount == 0)
		{
			dircount = 1;
			return 1;
		}
		else if (ballPos[0].position.x < ballPos[1].position.x && dircount == 1)
		{
			return 1;
		}
	}
	return 0;
}

function ballCollision(scene)
{
	let A = 0;
	let B = 0;
	let collision = 0;
	let bounce = 0;
	let bouncecount = 0;
	let savecollx = 0;
	let savecollz = 0;
	let endline = 0;
	let points2 = [];

	A = (ballPos[1].position.z - ballPos[0].position.z) / (ballPos[1].position.x - ballPos[0].position.x);
	B = ballPos[0].position.z - A * ballPos[0].position.x;
	collision = A * 10 + B;

	while (collision > 10 || collision < -10)
	{
		if (collision > 10)
		{
			savecollx = (10 - B) / A;
			savecollz = 10;

			bounce = (10 - B) / A;
			A = A * -1;
			B = 10 - (A * bounce);
		}
		else if (collision < -10)
		{
			savecollx = (-10 - B) / A;
			savecollz = -10;

			bounce = (-10 - B) / A;
			A = A * -1;
			B = -10 - (A * bounce);
		}

		bouncecount++;
		collision = A * 10 + B;

		endline = 10;
		if (collision > 10 || collision < -10)
		{
			if (collision > 10)
			{
				endline = (10 - B) / A;
			}
			else if (collision < -10)
			{
				endline = (-10 - B) / A;
			}
		}
	}
	return (collision);
}

