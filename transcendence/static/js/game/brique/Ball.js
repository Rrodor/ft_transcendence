//Ball.js
const ballBoundingBox = new THREE.Box3();

export function initBall(scene, positionZ)
{
	const ballGeometry = new THREE.SphereGeometry(0.2, 32, 32);
	const ballMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
	const ball = new THREE.Mesh(ballGeometry, ballMaterial);
	ballBoundingBox.setFromObject(ball);
	ball.position.set(0, 0, positionZ - 0.5);
	ball.castShadow = true;
	ball.receiveShadow = true;
	scene.add(ball);
	ball.velocity = initBallVelocity();
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

function initBallVelocity()
{
	// Convert degrees to radians
	const degToRad = (degrees) => degrees * (Math.PI / 180);

	// Define the angle ranges
	const minAngle = degToRad(-30);
	const maxAngle = degToRad(30);

	// Randomly choose an angle between -30 and +30 degrees
	const randomAngle = minAngle + Math.random() * (maxAngle - minAngle);

	// Calculate the forward vector (upwards from the ground)
	// Assuming the forward vector is the negative Z-axis
	let forward = new THREE.Vector3(0, 0, -1);

	// Create a rotation axis perpendicular to the forward direction
	// Assuming the Y-axis as the rotation axis
	let rotationAxis = new THREE.Vector3(0, 1, 0);

	// Create a quaternion for the rotation
	let quaternion = new THREE.Quaternion();
	quaternion.setFromAxisAngle(rotationAxis, randomAngle);

	// Apply the quaternion to the forward vector
	forward.applyQuaternion(quaternion);

	// Set the speed and calculate the velocity
	const speed = 0.1;
	let ballVelocity = forward.multiplyScalar(speed);

	return ballVelocity;
}


export function move(ball)
{
	ball.position.add(ball.velocity);
}

export function resetBall(ball, positionZ)
{
	ball.position.set(0, 0, positionZ - 0.5);
	ball.velocity = initBallVelocity(ball);
}

export { ballBoundingBox }
