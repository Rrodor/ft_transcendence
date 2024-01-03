export function initBall()
{
	// Ball geometry
	const ballGeometry = new THREE.SphereGeometry(0.2, 32, 32);
	const ballMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
	const ball = new THREE.Mesh(ballGeometry, ballMaterial);
	ball.position.set(0, 0, 0);
	ball.castShadow = true;
	ball.receiveShadow = true;

	return { ball, ballGeometry, ballMaterial };
}
