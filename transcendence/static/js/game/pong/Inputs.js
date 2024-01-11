//Inputs.js
function initInputs()
{
	let inputs =
	{
		movePaddleLeftUp: false,
		movePaddleLeftDown: false,
		movePaddleRightUp: false,
		movePaddleRightDown: false,
		sendInfosToServer: false
	};

	window.addEventListener('keydown', (event) => handleKeyDown(event, inputs));
	window.addEventListener('keyup', (event) => handleKeyUp(event, inputs));

	return inputs;
}

function handleKeyDown(event, inputs)
{
	switch (event.key.toLowerCase()) {
		case 'q':
			inputs.movePaddleLeftUp = true;
			break;
		case 'a':
			inputs.movePaddleLeftDown = true;
			break;
		case 'p':
			inputs.movePaddleRightUp = true;
			break;
		case 'l':
			inputs.movePaddleRightDown = true;
			break;
		case 's':
			inputs.sendInfosToServer = true;
			break;
	}
}

function handleKeyUp(event, inputs)
{
	switch (event.key.toLowerCase()) {
		case 'q':
			inputs.movePaddleLeftUp = false;
			break;
		case 'a':
			inputs.movePaddleLeftDown = false;
			break;
		case 'p':
			inputs.movePaddleRightUp = false;
			break;
		case 'l':
			inputs.movePaddleRightDown = false;
			break;
		case 's':
			inputs.sendInfosToServer = false;
			break;
	}
}

export { initInputs };
