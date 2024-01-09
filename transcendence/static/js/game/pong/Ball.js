//Ball.js
const ballBoundingBox = new THREE.Box3();

export function initBall(scene)
{
	const ballGeometry = new THREE.SphereGeometry(0.2, 32, 32);
	const ballMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
	const ball = new THREE.Mesh(ballGeometry, ballMaterial);
	ballBoundingBox.setFromObject(ball);
	ball.position.set(0, 0, 0);
	ball.castShadow = true;
	ball.receiveShadow = true;
	scene.add(ball);
	ball.velocity = initBallVelocity(ball);
	return { ball };
}

export function getBallPosition(ball)
{
	return ball.position;
}

export function getBallVelocity(ball)
{
	return ball.velocity;
}

export function setBallPosition(ball, position)
{
	ball.position.set(position.x, position.y, position.z);
}

export function setBallVelocity(ball, velocity)
{
	ball.velocity = velocity;
}

function initBallVelocity(ball)
{
	// Convert degrees to radians
	const degToRad = (degrees) => degrees * (Math.PI / 180);

	// Define the angle ranges
	const angleClamp = 80;
	const minRightAngle = degToRad(0 + angleClamp);
	const maxRightAngle = degToRad(180 - angleClamp);
	const minLeftAngle = degToRad(180 + angleClamp);
	const maxLeftAngle = degToRad(0 - angleClamp);

	// Randomly choose between the right and left side ranges
	const isRightSide = Math.random() < 0.5;
	const randomAngle = isRightSide
		? minRightAngle + Math.random() * (maxRightAngle - minRightAngle)
		: minLeftAngle + Math.random() * (maxLeftAngle - minLeftAngle);

	// Apply the rotation to the ball (around the Y-axis)
	ball.rotation.y = randomAngle;

	// Calculate the forward vector
	const forward = new THREE.Vector3(0, 0, -1);
	forward.applyQuaternion(ball.quaternion);

	// Set the speed and calculate the velocity
	const speed = 0.1;
	let ballVelocity = forward.multiplyScalar(speed);

	return ballVelocity;
}

export function move(ball)
{
	ball.position.add(ball.velocity);
}

export function resetBall(ball)
{
	ball.position.set(0, 0, 0);
	ball.velocity = initBallVelocity(ball);
}

export { ballBoundingBox }
