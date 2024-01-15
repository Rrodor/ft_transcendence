//Inputs.js
function initInputs()
{
	let inputs =
	{
		movePaddleLeft: false,
		movePaddleRight: false
	};

	window.addEventListener('keydown', (event) => handleKeyDown(event, inputs));
	window.addEventListener('keyup', (event) => handleKeyUp(event, inputs));

	return inputs;
}

function handleKeyDown(event, inputs)
{
	switch (event.key.toLowerCase())
	{
		case 'a':
			inputs.movePaddleLeft = true;
			break;
		case 'd':
			inputs.movePaddleRight = true;
			break;
	}
}

function handleKeyUp(event, inputs)
{
	switch (event.key.toLowerCase())
	{
		case 'a':
			inputs.movePaddleLeft = false;
			break;
		case 'd':
			inputs.movePaddleRight = false;
			break;
	}
}

export { initInputs };
