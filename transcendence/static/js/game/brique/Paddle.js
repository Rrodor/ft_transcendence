export function initPaddle(scene, position)
{
	const paddleGeometry = new THREE.BoxGeometry(2, 0.3, 0.3);
	const paddleMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
	const paddle = new THREE.Mesh(paddleGeometry, paddleMaterial);
	const paddleBoundingBox = new THREE.Box3().setFromObject(paddle);

	paddle.position.set(position.x, position.y, position.z);
	paddle.castShadow = true;
	paddle.receiveShadow = true;

	scene.add(paddle);

	return { paddle, paddleBoundingBox };
}
