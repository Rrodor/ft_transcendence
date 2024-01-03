export function initScene()
{
	// Scene setup
	const scene = new THREE.Scene();

	// Camera setup
	const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
	camera.position.set(0, 10, 0); // Position 10 units above the ground
	camera.lookAt(new THREE.Vector3(0, 0, 0)); // Look at the center of the scene

	// Renderer setup
	const renderer = new THREE.WebGLRenderer({ antialias: true });
	renderer.setSize(window.innerWidth, window.innerHeight);
	renderer.shadowMap.enabled = true;
	document.body.appendChild(renderer.domElement);

	// Background setup
	renderer.setClearColor(0x111111); // Set to a gray color

	// Resize canvas on resize window
	window.addEventListener('resize', () => {
		camera.aspect = window.innerWidth / window.innerHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(window.innerWidth, window.innerHeight);
	});

	return { scene, camera, renderer };
}
