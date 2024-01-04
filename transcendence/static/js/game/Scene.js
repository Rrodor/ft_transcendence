export function initScene()
{
	// Scene setup
	const scene = new THREE.Scene();

	// Camera setup
	const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
	camera.rotation.x = -Math.PI / 2;
	camera.position.set(0, 20, 0);

	// Renderer setup
	const renderer = new THREE.WebGLRenderer({ antialias: true });
	renderer.setSize(window.innerWidth, window.innerHeight);
	renderer.shadowMap.enabled = true;
	document.body.appendChild(renderer.domElement);

	// Background setup
	renderer.setClearColor(0x111111); // Set to a gray color

	return { scene, camera, renderer };
}
