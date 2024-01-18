//Scene.js
import * as Envi from './Environment.js';
import * as Time from './Time.js';
import * as Game from './Game.js';

if (match === 1)
{
	console.log(player1_name + " vs " + player2_name);
}

export function initScene()
{
	// Setup the scene
	const scene = new THREE.Scene();

	// Setup the camera
	const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
	camera.rotation.x = -Math.PI / 2.5;
	camera.position.set(0, 20, 10);

	// Setup the renderer
	const renderer = new THREE.WebGLRenderer({ antialias: true });
	renderer.setSize(window.innerWidth, window.innerHeight);
	renderer.shadowMap.enabled = true;
	document.body.appendChild(renderer.domElement);

	// Setup resize handler
	setupResizeHandler(camera, renderer);

	// Setup the environment
	let environmentBoundingBoxes = Envi.init(scene, camera);

	return { scene, camera, renderer, environmentBoundingBoxes};
}

export function setupResizeHandler(camera, renderer)
{
	window.addEventListener('resize', () => {
		camera.aspect = window.innerWidth / window.innerHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(window.innerWidth, window.innerHeight);
	});
}

export function animateGame(renderer, scene, camera)
{
	function animate(time)
	{
		requestAnimationFrame(animate); // Request next frame
		Game.update(scene, Time.getDeltaTime(time)); // Update game state
		renderer.render(scene, camera); // Render the scene
	}
	animate();
}

/*
	let seconds = 0;
	Pong request every seconds
	seconds = Math.round(time / 100);
	if (seconds % 10 === 0)
		sendBallPositionToServer({ x: ball.position.x, y: ball.position.y, z: ball.position.z });
*/
