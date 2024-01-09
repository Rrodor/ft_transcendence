const material = new THREE.LineBasicMaterial( { color: 0xff0000 } );
const material2 = new THREE.LineBasicMaterial( { color: 0x00ff00 } );


let elapsedTime = 1;
let dircount = 0;
let	paddlePos = 0;
let ballPos = [];

export function AImove(trueBallPos, truePaddlePos, paddleSpeed, deltaTime, scene)
{
	elapsedTime += deltaTime;
	let ballFinalPos = 0;
	let dirright = 0;

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
	}
	if (ballPos.lenght == 1)
	{
		//console.log("Alpha ballPos.z = " + ballPos[0].position.z);
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
		//console.log("Omega ballPos.z = " + ballPos[1].position.z);
		if (!dirright)
		{
			console.log("going to the left");
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
			console.log("going to the right long time");
			ballFinalPos = ballCollision(scene);
			//console.log("ballFinalPos = " + ballFinalPos);
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

function getDirection()
{
	if (ballPos.length == 2)
	{
		if (ballPos[0].position.x > ballPos[1].position.x)
		{
			console.log("going to the left");
			dircount = 0;
			return 0;
		}
		else if (ballPos[0].position.x < ballPos[1].position.x && dircount == 0)
		{
			console.log("going to the left ----------------------------");
			dircount = 1;
			return 0;
		}
		else if (ballPos[0].position.x < ballPos[1].position.x && dircount == 1)
		{
			console.log("going to the right");
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

	A = (ballPos[1].position.z - ballPos[0].position.z) / (ballPos[1].position.x - ballPos[0].position.x);
	B = ballPos[0].position.z - A * ballPos[0].position.x;
	//console.log("A = " + A);
	//console.log("B = " + B);

	collision = A * 10 + B;
	console.log("collision = " + collision);

	const points = [];
	points.push( ballPos[1].position.clone() );
	points.push( new THREE.Vector3(10, 0, A * 10 + B) );

	const geometry = new THREE.BufferGeometry().setFromPoints( points );
	const line = new THREE.Line( geometry, material );
	scene.add( line );
	points.shift();
	points.shift();

	while (collision > 10 || collision < -10)
	{
		if (collision > 10)
		{
			savecollx = (10 - B) / A;
			savecollz = 10;

			bounce = (10 - B) / A;
			console.log("A = " + A);
			A = A * -1;
			console.log("B = " + B);
			B = bounce - (A * 10);
		}
		else if (collision < -10)
		{
			savecollx = (-10 - B) / A;
			savecollz = -10;

			bounce = (-10 - B) / A;
			console.log("A = " + A);
			A = A * -1;
			console.log("B = " + B);
			B = bounce - (A * 10);
		}

		bouncecount++;
		collision = A * 10 + B;

		/*endline = 10;
		console.log("nextcollision = " + collision);
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
		}*/

		console.log(A + " * x + " + B + " = " + collision);
		const points2 = [];
		points2.push( new THREE.Vector3(savecollx, 0, savecollz) );
		points2.push( new THREE.Vector3(10, 0, collision) );

		const geometry = new THREE.BufferGeometry().setFromPoints( points2 );
		const line2 = new THREE.Line( geometry, material2 );
		scene.add( line2 );
		points2.shift();
		points2.shift();
	}
	//console.log("bouncecount = " + bouncecount);
	return (collision);
}

