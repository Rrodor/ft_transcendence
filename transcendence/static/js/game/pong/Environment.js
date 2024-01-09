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

export function initPlaceHolders(scene)
{
	const geoBigBox = new THREE.BoxGeometry(40, 3, 5);
	const geoSmallBox = new THREE.BoxGeometry(5, 3, 20);
	const material = new THREE.MeshPhongMaterial({ color: 0x888888 });
	const meshBoxLeft = new THREE.Mesh(geoSmallBox, material);
	const meshBoxRight = new THREE.Mesh(geoSmallBox, material);
	const meshBoxTop = new THREE.Mesh(geoBigBox, material);
	const meshBoxBot = new THREE.Mesh(geoBigBox, material);

	meshBoxLeft.position.set(-17.5, 0, 0);
	meshBoxRight.position.set(17.5, 0, 0);
	meshBoxTop.position.set(0, 0, -12.5);
	meshBoxBot.position.set(0, 0, 12.5);

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
	const groundGeometry = new THREE.PlaneGeometry(30, 20);
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
	initGroundLines(scene);
	initLights(scene, camera);
	let placeHolders = initPlaceHolders(scene);
	return placeHolders;
}

export { boxBotBoundingBox, boxTopBoundingBox, boxLeftBoundingBox, boxRightBoundingBox }
