//Game.js
import * as Paddle from './Paddle.js';
import * as Ball from './Ball.js';
import * as Network from './Network.js';
import { initInputs } from './Inputs.js';
import { ballBoundingBox } from './Ball.js';
import { initBrick } from './Environment.js';
import { initScoreSprites, updateScoreSprite } from "./UserInterface.js";

let ball = null;
let paddle = null;
let paddleSpeed = 20;
let paddleBoundingBox = null;
let environmentBoundingBoxes = null;
let inputs = null;
let scoreSprite;
let score = 0;
let lifeLeft = 5;
let bricks = [];
let gameEnded = false;

export function init(scene, envBoundingBoxes)
{
	console.log("user_id: " + userId);
	const result = Paddle.initPaddle(scene, new THREE.Vector3(0, 0, 10));
	paddle = result.paddle;
	paddleBoundingBox = result.paddleBoundingBox;

	const initBall = Ball.initBall(scene, paddle.position.z);
	ball = initBall.ball;

	// Initialize a grid of bricks
	const rows = 10;
	const columns = 15;
	const brickWidth = 3; // Width of each brick
	const brickHeight = 1; // Height of each brick
	const padding = 0.01; // Space between bricks
	const startX = (((columns * brickWidth) * (-1)) + brickWidth) / 2; // Starting X position
	const startZ = -15 + 5 + brickHeight / 2; // Starting Z position

	// Brick value to color mapping
	const brickColors = {
		5: 0x00ff00,  // Green
		10: 0xff0000, // Red
		15: 0x0000ff, // Blue
		20: 0xffff00, // Yellow
		25: 0x333333  // Light black
	};

	// Calculate the number of bricks for each value
	const totalBricks = rows * columns;
	const totalValue = 2250;
	const values = [5, 10, 15, 20, 25];
	const bricksCount = values.map(value => Math.floor(totalValue / value / totalBricks));

	for (let i = 0; i < rows; i++) {
		for (let j = 0; j < columns; j++) {
			const x = startX + j * (brickWidth + padding);
			const z = startZ + i * (brickHeight + padding);
			const brickValueIndex = Math.floor(Math.random() * bricksCount.length);
			const brickValue = values[brickValueIndex];
			const brickPosition = new THREE.Vector3(x, 0.5, z);
			const color = brickColors[brickValue];
			const { meshBrick, brickSprite, brickBoundingBox } = initBrick(scene, brickValue, brickPosition, color);
			bricks.push({ meshBrick, brickSprite, brickBoundingBox, value: brickValue });
		}
	}

	environmentBoundingBoxes = envBoundingBoxes;

	inputs = initInputs();

	scoreSprite = initScoreSprites(scene, new THREE.Vector3(0, 10, -6.5), new THREE.Vector3(1.5, 1.5, 1.5));
}

export function update(scene, deltaTime)
{
	//if (!ball || !paddle) return;

	Ball.move(ball);
	movePaddles(deltaTime);
	checkCollision(scene, ball, paddle);
	checkBallPosition(ball, paddle);
	updateScoreSprite(scoreSprite, score);
}

function checkBallPosition(ball, paddle)
{
	if (ball.position.z > 12.5)
	{
		Ball.resetBall(ball, paddle.position.z);
		lifeLeft--;
		if (lifeLeft == 0)
		{
			endGame();
		}
	}
}

function movePaddles(deltaTime)
{
	let delta = deltaTime * paddleSpeed;

	if (inputs.movePaddleRight && paddle.position.x < 21.5)
		paddle.position.x += delta;
	if (inputs.movePaddleLeft && paddle.position.x > -21.5)
		paddle.position.x -= delta;
}

function checkCollision(scene, ball, paddle)
{
	//if (!environmentBoundingBoxes) return;

	ballBoundingBox.setFromObject(ball);
	paddleBoundingBox.setFromObject(paddle);

	if (ballBoundingBox.intersectsBox(paddleBoundingBox))
		adjustBallVelocity(ball, paddle);

	// Check collision with the side walls
	let currentVelocity = Ball.getBallVelocity(ball);
	if (ball.position.x < environmentBoundingBoxes.boxLeftBoundingBox.max.x)
		currentVelocity.x *= -1;
	if (ball.position.x > environmentBoundingBoxes.boxRightBoundingBox.min.x)
		currentVelocity.x *= -1;
	if (ball.position.z < environmentBoundingBoxes.boxBotBoundingBox.min.z)
		currentVelocity.z *= -1;
	if (ball.position.z > environmentBoundingBoxes.boxTopBoundingBox.max.z)
		currentVelocity.z *= -1;
	Ball.setBallVelocity(ball, currentVelocity);

	// Check collision with bricks
	for (let i = bricks.length - 1; i >= 0; i--)
	{
		const brick = bricks[i];
		ballBoundingBox.setFromObject(ball);

		if (ballBoundingBox.intersectsBox(brick.brickBoundingBox))
		{
			score += brick.value;

			// Remove brick from scene
			scene.remove(brick.meshBrick);
			scene.remove(brick.brickSprite);

			// Remove brick from the array
			bricks.splice(i, 1);

			// Adjust ball velocity
			ball.velocity.z *= -1; // Example adjustment, modify as needed

			break; // Exit loop after collision
		}
	}

	if (score == 2250)
		console.log("You Win !");

}

function adjustBallVelocity(ball, paddle)
{
	ball.velocity.z *= -1;
	let hitPoint = (ball.position.x - paddle.position.x) / paddle.scale.x;
	hitPoint = Math.max(-1, Math.min(1, hitPoint));
	ball.velocity.x += hitPoint * 0.05;
	ball.velocity.normalize().multiplyScalar(0.1);
}

function sendInfosToServer() {
	Network.sendScore(score, userId);
}

function endGame() {
    if (gameEnded) return; // Empêche les appels multiples
    gameEnded = true;

    sendInfosToServer();
    window.setTimeout(() => {
        window.location.href = "/brique/end_game/";
    }, 1); // Délai avant la redirection pour permettre l'envoi des données
}
