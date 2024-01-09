//Paddle.js
//import * from "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.js";

//import * from "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/jsm/loaders/GLTFLoader.js";
/*
export function initPaddle(scene, position, modelPath)
{
    const loader = new GLTFLoader();

    // Placeholder for the paddle
    let paddle = new THREE.Object3D();
    const paddleBoundingBox = new THREE.Box3();

    loader.load(modelPath, (gltf) => {
        paddle = gltf.scene.children[0]; // Assuming the paddle is the first object in the GLTF scene
        paddle.position.set(position.x, position.y, position.z);
        paddle.rotation.y = Math.PI / 2;
        paddle.castShadow = true;
        paddle.receiveShadow = true;

        paddleBoundingBox.setFromObject(paddle);
        scene.add(paddle);
    }, undefined, (error) => {
        console.error('An error happened during loading the model:', error);
    });

    return { paddle, paddleBoundingBox };
}*/

export function initPaddle(scene, position)
{
	const paddleGeometry = new THREE.BoxGeometry(2, 0.3, 0.3);
	const paddleMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
	const paddle = new THREE.Mesh(paddleGeometry, paddleMaterial);
	const paddleBoundingBox = new THREE.Box3().setFromObject(paddle);

	paddle.position.set(position.x, position.y, position.z);
	paddle.rotation.y = Math.PI / 2;
	paddle.castShadow = true;
	paddle.receiveShadow = true;

	scene.add(paddle);

	/*

	const paddle = assetManager.getAsset('paddle');
	if (paddle)
	{
		const paddleBoundingBox = new THREE.Box3().setFromObject(new THREE.BoxGeometry(2, 0.3, 0.3));
		paddle.position.set(position.x, position.y, position.z);
		paddle.rotation.y = Math.PI / 2;
		paddle.castShadow = true;
		paddle.receiveShadow = true;
		scene.add(paddle);
	}*/

	return { paddle, paddleBoundingBox };
}
