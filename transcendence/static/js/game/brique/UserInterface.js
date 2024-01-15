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

function createBrickTexture(text, fontSize = 100, fontFace = 'Arial', textColor = 'white', backgroundColor = 'rgba(0, 0, 0, 0)')
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

	const textX = canvas.width / 2;
	const textY = canvas.height / 2;

	context.fillText(text, textX, textY);
	return new THREE.CanvasTexture(canvas);
}

function updateScoreSprite(sprite, newScore)
{
	const newScoreText = newScore.toString();
	const newTexture = createTextTexture(newScoreText);
	sprite.material.map = newTexture;
	sprite.material.needsUpdate = true;
}

function initScoreSprites(scene, position, scale)
{
	const scoreSpriteMaterial = new THREE.SpriteMaterial({ map: createTextTexture("0") });
	const scoreSprite = new THREE.Sprite(scoreSpriteMaterial);

	scoreSprite.scale.set(scale.x, scale.y, scale.z);
	scoreSprite.position.set(position.x, position.y, position.z);

	scene.add(scoreSprite);

	return scoreSprite;
}

function initBrickSprite(scene, brickValue, position, scale)
{
	const spriteMaterial = new THREE.SpriteMaterial({ map: createBrickTexture(brickValue.toString()) });
	const sprite = new THREE.Sprite(spriteMaterial);

	sprite.scale.set(scale.x, scale.y, scale.z);
	sprite.position.set(position.x, position.y, position.z);

	scene.add(sprite);

	return sprite;
}

export { initScoreSprites, updateScoreSprite, initBrickSprite};

/*
	scoreSprite.scale.set(1.75, 1.75, 1.75);
	scoreSprite.position.set(-2, 10, -6.5);
*/
