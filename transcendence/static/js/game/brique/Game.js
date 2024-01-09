//Game.js
import * as Paddle from './Paddle.js';
import * as Ball from './Ball.js';
import { initInputs } from './Inputs.js';
import { ballBoundingBox } from './Ball.js';
// import { initScoreSprites, updateScoreSprite } from "./UserInterface.js";
//import assetManager from './AssetManager.js';

let ball = null;
let paddle = null;
let paddleSpeed = 20;
let paddleBoundingBox = null;
let environmentBoundingBoxes = null;
let inputs = null;
let scoreSprite;
let score = 5;

export function init(scene, envBoundingBoxes)
{
	const result = Paddle.initPaddle(scene, new THREE.Vector3(0, 0, 10));
	paddle = result.paddle;
	paddleBoundingBox = result.paddleBoundingBox;

	const initBall = Ball.initBall(scene, paddle.position.z);
	ball = initBall.ball;

	environmentBoundingBoxes = envBoundingBoxes;

	inputs = initInputs();

	//scoreSprite = initScoreSprites(scene, new THREE.Vector3(-2, 10, -6.5), new THREE.Vector3(1.75, 1.75, 1.75));
}

export function update(scene, deltaTime)
{
	if (!ball || !paddle) return;

	Ball.move(ball);
	movePaddles(deltaTime);
	checkCollision(ball, paddle);
	checkBallPosition(ball, paddle);
	//updateScoreSprite(scoreSprite, score);
}

function checkBallPosition(ball, paddle)
{
	if (ball.position.z > 10)
	{
		Ball.resetBall(ball, paddle.position.z);
		score--;
		if (score == 0)
		{
			console.log("Game Over");
		}
	}
}

function movePaddles(deltaTime)
{
	let delta = deltaTime * paddleSpeed;

	if (inputs.movePaddleRight && paddle.position.x > -8.75)
		paddle.position.x -= delta;
	if (inputs.movePaddleLeft && paddle.position.x < 8.75)
		paddle.position.x += delta;
}

function checkCollision(ball, paddle)
{
	if (!environmentBoundingBoxes) return;

	ballBoundingBox.setFromObject(ball);
	paddleBoundingBox.setFromObject(paddle);

	if (ballBoundingBox.intersectsBox(paddleBoundingBox))
		adjustBallVelocity(ball, paddle);

	// Check collision with the side walls
	let currentVelocity = Ball.getBallVelocity(ball);

	if (ball.position.x < -15)
		currentVelocity.x *= -1;
	if (ball.position.x > 15)
		currentVelocity.x *= -1;
	if (ball.position.z < -15)
		currentVelocity.z *= -1;

	Ball.setBallVelocity(ball, currentVelocity);

}

function adjustBallVelocity(ball, paddle)
{
	let hitPoint = (ball.position.z - paddle.position.z) / paddle.scale.z;
	hitPoint = Math.max(-1, Math.min(1, hitPoint));

	// Clamp the angle range to prevent extreme angles
	const maxAngleRange = Math.PI / 6; // 30 degrees max angle
	let angle = maxAngleRange * hitPoint;

	// Reverse the horizontal direction
	ball.velocity.x *= -1;

	// Adjust the vertical direction based on the hit point
	// Prevent extreme vertical velocity changes
	ball.velocity.z = Math.tan(angle) * Math.abs(ball.velocity.x);

	// Normalize the velocity to maintain consistent speed
	ball.velocity.normalize().multiplyScalar(0.1); // Adjust the 0.1 speed value as needed
}
