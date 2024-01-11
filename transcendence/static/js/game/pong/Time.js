let lastTime = 0;

export function getLastTime()
{
	return lastTime;
}

export function setLastTime(time)
{
	lastTime = time;
}

export function getDeltaTime(time)
{
	let deltaTime = (time - getLastTime()) / 1000;
	setLastTime(time);

	return deltaTime;
}
