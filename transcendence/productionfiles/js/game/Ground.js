export function initGround()
{
	const groundGeometry = new THREE.PlaneGeometry(30, 20);
	const groundMaterial = new THREE.MeshPhongMaterial({ color: 0x222222 });
	const ground = new THREE.Mesh(groundGeometry, groundMaterial);
	ground.position.set(0, -0.1, 0);
	ground.rotation.x = -Math.PI / 2;
	ground.receiveShadow = true;

	return { ground, groundGeometry, groundMaterial };
}
