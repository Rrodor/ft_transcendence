export function initLights(camera)
{
	const light = new THREE.DirectionalLight(0xffffff, 0.5);
	light.position.copy(camera.position);
	light.castShadow = true;

	return { light };
}
