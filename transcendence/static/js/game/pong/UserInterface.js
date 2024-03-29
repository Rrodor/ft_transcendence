// UserInterface.js
function createTextTexture(text, fontSize = 100, fontFace = 'Arial', textColor = 'white', backgroundColor = 'black')
{
	const canvas = document.createElement('canvas');
	const context = canvas.getContext('2d');
	canvas.width = 256;
	canvas.height = 256;
	context.fillStyle = backgroundColor;
	context.fillRect(0, 0, canvas.width, canvas.height);
	context.font = `${fontSize}px ${fontFace}`;
	context.fillStyle = textColor;
	context.textAlign = 'center';
	context.textBaseline = 'middle';
	context.fillText(text, canvas.width / 2, canvas.height / 2);
	return new THREE.CanvasTexture(canvas);
}

function updateSprite(sprite, newScore)
{
	const newScoreText = newScore.toString();
	const newTexture = createTextTexture(newScoreText);
	sprite.material.map = newTexture;
	sprite.material.needsUpdate = true;
}

function initSprite(scene, position, scale)
{
	const scoreSpriteMaterial = new THREE.SpriteMaterial({ map: createTextTexture("0") });
	const scoreSprite = new THREE.Sprite(scoreSpriteMaterial);

	scoreSprite.scale.set(scale.x, scale.y, scale.z);
	scoreSprite.position.set(position.x, position.y, position.z);

	scene.add(scoreSprite);

	return scoreSprite;
}

export { initSprite, updateSprite };

function createNameTexture(text, fontSize = 100, fontFace = 'Arial', textColor = 'white', backgroundColor = 'black')
{
	const canvas = document.createElement('canvas');
	const context = canvas.getContext('2d');
	canvas.width = 512;
	canvas.height = 256;
	context.fillStyle = backgroundColor;
	context.fillRect(0, 0, canvas.width, canvas.height);
	context.font = `${fontSize}px ${fontFace}`;
	context.fillStyle = textColor;
	context.textAlign = 'center';
	context.textBaseline = 'middle';
	context.fillText(text, canvas.width / 2, canvas.height / 2);
	return new THREE.CanvasTexture(canvas);
}

function initNameSprites(scene, position, scale, name)
{
    const nameSpriteMaterial = new THREE.SpriteMaterial({ map: createTextTexture("0") });
    const nameSprite = new THREE.Sprite(nameSpriteMaterial);

    nameSprite.scale.set(scale.x, scale.y, scale.z);
    nameSprite.position.set(position.x, position.y, position.z);

    scene.add(nameSprite);

	const newTexture = createNameTexture(name);
	nameSprite.material.map = newTexture;
    return nameSprite; // Return the sprite directly
}

export { initNameSprites };

/*
	scoreSprite.scale.set(1.75, 1.75, 1.75);
	scoreSprite.position.set(-2, 10, -6.5);
*/