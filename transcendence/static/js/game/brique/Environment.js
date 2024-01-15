//environment.js
import { initLights } from './Lights.js';
import { initBrickSprite } from "./UserInterface.js";

const boxBotBoundingBox = new THREE.Box3();
const boxTopBoundingBox = new THREE.Box3();
const boxLeftBoundingBox = new THREE.Box3();
const boxRightBoundingBox = new THREE.Box3();

function degToRad(degrees)
{
	return degrees * Math.PI / 180;
}

export function initBrick(scene, brickValue, brickPosition, color)
{
	const geoBrick = new THREE.BoxGeometry(3, 1, 1);
	const material = new THREE.MeshPhongMaterial({ color: new THREE.Color(color) });
	const meshBrick = new THREE.Mesh(geoBrick, material);

	meshBrick.position.set(brickPosition.x, brickPosition.y, brickPosition.z);
	scene.add(meshBrick);

	const spriteScale = new THREE.Vector3(1, 1, 1);
	const spritePosition = new THREE.Vector3(brickPosition.x - 0.1, brickPosition.y + 0.5, brickPosition.z);
	const brickSprite = initBrickSprite(scene, brickValue, spritePosition, spriteScale);

	// Create a bounding box for the brick
	const brickBoundingBox = new THREE.Box3().setFromObject(meshBrick);

	return { meshBrick, brickSprite, brickBoundingBox };
}

export function initBorders(scene)
{
	const geoBigBox = new THREE.BoxGeometry(60, 1, 10);
	const geoSmallBox = new THREE.BoxGeometry(5, 1, 30);
	const material = new THREE.MeshPhongMaterial({ color: 0x222222 });
	const meshBoxLeft = new THREE.Mesh(geoSmallBox, material);
	const meshBoxRight = new THREE.Mesh(geoSmallBox, material);
	const meshBoxTop = new THREE.Mesh(geoBigBox, material);
	const meshBoxBot = new THREE.Mesh(geoBigBox, material);

	meshBoxLeft.position.set(-25, 0.5, 5);
	meshBoxRight.position.set(25, 0.5, 5);
	meshBoxTop.position.set(0, 0.5, -15);
	meshBoxBot.position.set(0, 0.5, 30);

	scene.add(meshBoxBot);
	scene.add(meshBoxTop);
	scene.add(meshBoxLeft);
	scene.add(meshBoxRight);

	return {
		boxBotBoundingBox: new THREE.Box3().setFromObject(meshBoxBot),
		boxTopBoundingBox: new THREE.Box3().setFromObject(meshBoxTop),
		boxLeftBoundingBox: new THREE.Box3().setFromObject(meshBoxLeft),
		boxRightBoundingBox: new THREE.Box3().setFromObject(meshBoxRight),
	};
}

export function initGround(scene)
{
	const groundGeometry = new THREE.PlaneGeometry(100, 100);
	const groundMaterial = new THREE.MeshPhongMaterial({ color: 0x222222 });
	const ground = new THREE.Mesh(groundGeometry, groundMaterial);

	ground.position.set(0, 0, 0);
	ground.rotation.x = -Math.PI / 2;
	ground.receiveShadow = true;

	scene.add(ground);
}

export function initGroundLines(scene)
{
	const planeGeometryLong = new THREE.PlaneGeometry(50, 0.1);
	const planeMaterial = new THREE.MeshBasicMaterial({ color: 0x555555 });
	const lineBot = new THREE.Mesh(planeGeometryLong, planeMaterial);

	lineBot.position.set(0, 0.001, 12.5);
	lineBot.rotation.x = degToRad(-90);

	scene.add(lineBot);
}

export function init(scene, camera)
{
	initGround(scene);
	initLights(scene, camera);
	initGroundLines(scene);
	let bordersBoundingBox = initBorders(scene);

	return bordersBoundingBox;
}

export { boxBotBoundingBox, boxTopBoundingBox, boxLeftBoundingBox, boxRightBoundingBox }
