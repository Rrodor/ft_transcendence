export function initPaddle(posX, posY, posZ)
{
	const paddleGeometry = new THREE.BoxGeometry(2, 0.3, 0.3);
	const paddleMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
	const paddle = new THREE.Mesh(paddleGeometry, paddleMaterial);
	paddle.position.set(posX, posY, posZ);
	paddle.rotation.y = Math.PI / 2;
	paddle.castShadow = true;
	paddle.receiveShadow = true;

	return { paddle };
}
