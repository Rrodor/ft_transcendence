export function initLights(camera)
{
	const dl = new THREE.DirectionalLight(0xffffff, 0.6);
	dl.position.copy(camera.position);
	dl.castShadow = true;

	return { dl };
}
