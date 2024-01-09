export function initLights(scene, camera)
{
	const dl = new THREE.DirectionalLight(0xffffff, 0.6);
	dl.position.copy(camera.position);
	dl.castShadow = true;

	for (let i = 0; i < 3; i++)
	{
		for (let j = 0; j < 2; j++)
		{
			const pointLight = new THREE.PointLight(0xffffff, 0.25, 100);
			pointLight.position.set(-20 + i * 20, 10, -10 + j * 20);
			scene.add(pointLight);
		}
	}

	scene.add(dl);
}
