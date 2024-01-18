//Game.js
import * as Paddle from './Paddle.js';
import * as Ball from './Ball.js';
import * as Network from './Network.js';
import { initInputs } from './Inputs.js';
import { ballBoundingBox } from './Ball.js';
import { initScoreSprites, updateScoreSprite , initNameSprites } from "./UserInterface.js";
import { AImove } from './AI.js';
//import assetManager from './AssetManager.js';

let ball = null;

let paddleLeft = null;
let paddleRight = null;
let paddleSpeed = 20;

let savedVelocity = null;

let inputs = null;

let environmentBoundingBoxes = null;
let paddleLeftBoundingBox = null;
let paddleRightBoundingBox = null;

let scoreLeftSprite, scoreRightSprite;
let nameLeftSprite, nameRightSprite;

if (is_ai === 1)
	console.log("AI is enabled");
else
	console.log("AI is disabled");

if (match !== 0)
	console.log("Match id: " + match_id);
else
	console.log("Match id: null");
let rightPlayerIsAI = false;

let scoreLeft = 0;
let scoreRight = 0;
let scoreAI = 0;
let scoreMax = 2;

let gameEnded = false;

export function init(scene, envBoundingBoxes, is_ai)
{
	const initBall = Ball.initBall(scene);
	ball = initBall.ball;

	const resultLeft = Paddle.initPaddle(scene, new THREE.Vector3(-10, 0.15, 0));
	paddleLeft = resultLeft.paddle;
	paddleLeftBoundingBox = resultLeft.paddleBoundingBox;

	const resultRight = Paddle.initPaddle(scene, new THREE.Vector3(10, 0.15, 0));
	paddleRight = resultRight.paddle;
	paddleRightBoundingBox = resultRight.paddleBoundingBox;

	environmentBoundingBoxes = envBoundingBoxes;

	inputs = initInputs();

	scoreLeftSprite = initScoreSprites(scene, new THREE.Vector3(-2, 7.5, -5), new THREE.Vector3(1.75, 1.75, 1.75));
	scoreRightSprite = initScoreSprites(scene, new THREE.Vector3(2, 7.5, -5), new THREE.Vector3(1.75, 1.75, 1.75));
	nameLeftSprite = initNameSprites(scene, new THREE.Vector3(-6, 7.5, -5), new THREE.Vector3(3.75, 1.75, 1.75), player1_name);
	nameRightSprite = initNameSprites(scene, new THREE.Vector3(6, 7.5, -5), new THREE.Vector3(3.75, 1.75, 1.75), player2_name);
}

export function update(scene, deltaTime)
{
	if (!ball || !paddleLeft || !paddleRight) return;

	Ball.move(ball);
	movePaddles(deltaTime);
	if (is_ai === 1)
		paddleRight.position.z = AImove(ball, paddleRight.position.z, paddleSpeed, deltaTime, scene);
	checkCollision(ball, paddleLeft, paddleRight);
	checkBallPosition(ball);
	updateScoreSprite(scoreLeftSprite, scoreLeft);
	updateScoreSprite(scoreRightSprite, scoreRight);
	if (scoreLeft > scoreMax || scoreRight > scoreMax)
	{
		endGame();
	}
}

function checkBallPosition(ball)
{
	if (ball.position.x < paddleLeft.position.x - 1)
	{
		scoreRight++;
		savedVelocity = Ball.resetBall(ball, savedVelocity);
	}
	if (ball.position.x > paddleRight.position.x + 1)
	{
		scoreLeft++;
		savedVelocity = Ball.resetBall(ball, savedVelocity);
	}
}

function movePaddles(deltaTime)
{
	let delta = deltaTime * paddleSpeed;

	if (inputs.movePaddleLeftUp && paddleLeft.position.z > -8.75)
		paddleLeft.position.z -= delta;
	if (inputs.movePaddleLeftDown && paddleLeft.position.z < 8.75)
		paddleLeft.position.z += delta;
	if (inputs.movePaddleRightUp && paddleRight.position.z > -8.75)
		paddleRight.position.z -= delta;
	if (inputs.movePaddleRightDown && paddleRight.position.z < 8.75)
		paddleRight.position.z += delta;
}

function checkCollision()
{
	if (!environmentBoundingBoxes) return;

	ballBoundingBox.setFromObject(ball);
	paddleLeftBoundingBox.setFromObject(paddleLeft);
	paddleRightBoundingBox.setFromObject(paddleRight);

	if (ballBoundingBox.intersectsBox(paddleLeftBoundingBox))
	{
		adjustBallVelocity(ball, paddleLeft);
	}

	if (ballBoundingBox.intersectsBox(paddleRightBoundingBox))
	{
		adjustBallVelocity(ball, paddleRight);
	}

	if (ballBoundingBox.intersectsBox(environmentBoundingBoxes.boxBotBoundingBox)) {
		let currentVelocity = Ball.getBallVelocity(ball);
		currentVelocity.z *= -1;
		Ball.setBallVelocity(ball, currentVelocity);
	}

	if (ballBoundingBox.intersectsBox(environmentBoundingBoxes.boxTopBoundingBox)) {
		let currentVelocity = Ball.getBallVelocity(ball);
		currentVelocity.z *= -1;
		Ball.setBallVelocity(ball, currentVelocity);
	}

	if (ballBoundingBox.intersectsBox(environmentBoundingBoxes.boxLeftBoundingBox)) {
		let currentVelocity = Ball.getBallVelocity(ball);
		currentVelocity.x *= -1;
		Ball.setBallVelocity(ball, currentVelocity);
	}

	if (ballBoundingBox.intersectsBox(environmentBoundingBoxes.boxRightBoundingBox)) {
		let currentVelocity = Ball.getBallVelocity(ball);
		currentVelocity.x *= -1;
		Ball.setBallVelocity(ball, currentVelocity);
	}
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
	//ball.velocity.normalize().multiplyScalar(0.1); // Adjust the 0.1 speed value as needed

	if (ball.velocity.length() < 0.1)
	{
		ball.velocity
		if (savedVelocity && savedVelocity.length() > 0.1)
			ball.velocity = savedVelocity;
		while (ball.velocity.length() < 0.1)
			ball.velocity.multiplyScalar(1.2);
	}
	ball.velocity.multiplyScalar(1.2);
	savedVelocity = ball.velocity;
}

function sendMatchInfosToServer()
{
	Network.sendMatchScore(scoreLeft, scoreRight, match_id);
}

function sendInfosToServer()
{
	Network.sendScore(scoreLeft, scoreRight, userId);
}

function endGame() {
    if (gameEnded) return; // Empêche les appels multiples
    gameEnded = true;

	if (match !== 0) {
		sendMatchInfosToServer();
		window.setTimeout(() => {
			window.location.href = "/pong/end_game/";
		}, 1);
		return;
	}

    sendInfosToServer();
    window.setTimeout(() => {
        window.location.href = "/pong/end_game/";
    }, 1);
}
