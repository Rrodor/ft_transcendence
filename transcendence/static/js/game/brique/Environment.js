//environment.js
import { initLights } from './Lights.js';

const boxBotBoundingBox = new THREE.Box3();
const boxTopBoundingBox = new THREE.Box3();
const boxLeftBoundingBox = new THREE.Box3();
const boxRightBoundingBox = new THREE.Box3();

function degToRad(degrees)
{
	return degrees * (Math.PI / 180);
}

export function initBricks(scene)
{
	const boxGeometry = new THREE.BoxGeometry(2, 0.4, 0.4);
	const boxMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
	const boxes = [];
	const numRows = 3;
	const numCols = 3;
	const spacing = 0.25;

	for (let row = 0; row < numRows; row++)
	{
		for (let col = 0; col < numCols; col++)
		{
			const box = new THREE.Mesh(boxGeometry, boxMaterial);
			const x = col * (boxGeometry.parameters.width + spacing) - (numCols * (boxGeometry.parameters.width) / 2);
			const z = row * (boxGeometry.parameters.depth + spacing) - 10;
			box.position.set(x, 0.2, z);
			box.castShadow = true;
			box.receiveShadow = true;
			scene.add(box);
			boxes.push({
				mesh: box,
				boxBoundingBox: new THREE.Box3().setFromObject(box)
			});
		}
	}

	return boxes;
}

export function initGround(scene)
{
	const groundGeometry = new THREE.PlaneGeometry(100, 100);
	const groundMaterial = new THREE.MeshPhongMaterial({ color: 0x222222 });
	const ground = new THREE.Mesh(groundGeometry, groundMaterial);

	ground.position.set(0, -0.2, 0);
	ground.rotation.x = -Math.PI / 2;
	ground.receiveShadow = true;

	scene.add(ground);
}

export function initGroundLines(scene)
{
	const planeGeometryLong = new THREE.PlaneGeometry(30, 0.1);
	const planeGeometryShort = new THREE.PlaneGeometry(20, 0.1);
	const planeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
	const lineBot = new THREE.Mesh(planeGeometryLong, planeMaterial);
	const lineTop = new THREE.Mesh(planeGeometryLong, planeMaterial);
	const lineLeft_1 = new THREE.Mesh(planeGeometryShort, planeMaterial);
	const lineLeft_2 = new THREE.Mesh(planeGeometryShort, planeMaterial);
	const lineRight_1 = new THREE.Mesh(planeGeometryShort, planeMaterial);
	const lineRight_2 = new THREE.Mesh(planeGeometryShort, planeMaterial);

	lineBot.position.set(0, 0, 9.95);
	lineBot.rotation.x = degToRad(-90);
	lineTop.position.set(0, 0, -9.95);
	lineTop.rotation.x = degToRad(-90);
	lineLeft_1.position.set(-14.95, 0, 0);
	lineLeft_1.rotation.x = degToRad(-90);
	lineLeft_1.rotation.z = degToRad(-90);
	lineLeft_2.position.set(-11, 0, 0);
	lineLeft_2.rotation.x = degToRad(-90);
	lineLeft_2.rotation.z = degToRad(-90);
	lineRight_1.position.set(14.95, 0, 0);
	lineRight_1.rotation.x = degToRad(-90);
	lineRight_1.rotation.z = degToRad(-90);
	lineRight_2.position.set(11, 0, 0);
	lineRight_2.rotation.x = degToRad(-90);
	lineRight_2.rotation.z = degToRad(-90);

	scene.add(lineBot);
	scene.add(lineTop);
	scene.add(lineLeft_1);
	scene.add(lineLeft_2);
	scene.add(lineRight_1);
	scene.add(lineRight_2);
}

export function init(scene, camera)
{
	initGround(scene);
	//initGroundLines(scene);
	initLights(scene, camera);
	let placeHolders = initBricks(scene);
	return placeHolders;
}

export { boxBotBoundingBox, boxTopBoundingBox, boxLeftBoundingBox, boxRightBoundingBox }
