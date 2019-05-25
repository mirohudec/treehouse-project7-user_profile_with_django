window.onload = () => {
	canvas = document.getElementById('canvas');
	container = document.getElementById('container');
	footer = document.getElementById('buttons');
	resizeContainer = document.getElementById('resize-container');
	resizeNE = document.getElementById('resize-ne');
	resizeNW = document.getElementById('resize-nw');
	resizeSE = document.getElementById('resize-se');
	resizeSW = document.getElementById('resize-sw');
	resizeNE.addEventListener('drag', (e) => {
		resizeDrag(e);
	});
	resizeNW.addEventListener('drag', (e) => {
		resizeDrag(e);
	});
	resizeSE.addEventListener('drag', (e) => {
		resizeDrag(e);
	});

	resizeSW.addEventListener('drag', (e) => {
		resizeDrag(e);
	});

	canvas.width = container.clientWidth;
	canvas.height = container.clientHeight - footer.clientHeight;
	canvasWidth = canvas.width;
	canvasHeight = canvas.height;
	ctx = canvas.getContext('2d');
	imageLoader = document.getElementById('input');
	imageLoader.addEventListener('change', (e) => {
		add(e, ctx);
	});
	rotateButton = document.getElementById('rotate');
	rotateButton.addEventListener('click', () => {
		rotate(ctx);
	});

	flipHButton = document.getElementById('flip_H');
	flipHButton.addEventListener('click', () => {
		flip_horizontally(ctx);
	});
	flipVButton = document.getElementById('flip_V');
	flipVButton.addEventListener('click', () => {
		flip_vertically(ctx);
	});
	cropperButton = document.getElementById('crop_image');
	cropperButton.addEventListener('click', () => {
		cropper(ctx);
	});
};

const init = (ctx) => {
	pictureWidth = image.width;
	pictureHeight = image.height;
	resizeContainer.style.left = canvasWidth / 2 - pictureWidth / 2 + 'px';
	resizeContainer.style.top = canvasHeight / 2 - pictureHeight / 2 + 'px';
	resizeContainer.style.width = image.width + 'px';
	resizeContainer.style.height = image.height + 'px';
	NW = new Point(
		canvasWidth / 2 - pictureWidth / 2,
		canvasHeight / 2 - pictureHeight / 2
	);
	SW = new Point(
		canvasWidth / 2 - pictureWidth / 2,
		canvasHeight / 2 - pictureHeight / 2 + img.height
	);
	NE = new Point(
		canvasWidth / 2 - pictureWidth / 2 + img.width,
		canvasHeight / 2 - pictureHeight / 2
	);
	SE = new Point(
		canvasWidth / 2 - pictureWidth / 2 + img.width,
		canvasHeight / 2 - pictureHeight / 2 + img.height
	);

	//new_resolution = calcNewSize(pictureWidth, pictureHeight, 500, 500);

	ctx.drawImage(
		image,
		canvasWidth / 2 - pictureWidth / 2,
		canvasHeight / 2 - pictureHeight / 2,
		dimensions.width,
		dimensions.height
	);
};

// resizing image to fit in 500 x 500 canvas while keeping its dimensions
const calcNewSize = (srcW, srcH, maxW, maxH) => {
	if (srcW < maxW && srcH < maxH) {
		return {
			width: srcW,
			height: srcH
		};
	}
	let ratio = Math.min(maxW / srcW, maxH / srcH);
	return {
		width: srcW * ratio,
		height: srcH * ratio
	};
};

class Point {
	constructor(x, y) {
		this.x = x;
		this.y = y;
	}
}

let img = new Image();
let dimension;
let image;
let canvasWidth;
let canvasHeight;
let pictureWidth;
let pictureHeight;
let resizeContainer;
let resizeNE, resizeNW, resizeSE, resizeSW;
let NE, NW, SE, SW;

const add = (e, ctx) => {
	let reader = new FileReader();
	reader.onload = (event) => {
		img.onload = () => {
			dimensions = calcNewSize(img.width, img.height, 500, 500);
			image = new Image(dimensions.width, dimensions.height);
			image.src = img.src;
			init(ctx);
		};
		img.src = event.target.result;
	};
	reader.readAsDataURL(e.target.files[0]);
};

const rotate = (ctx) => {
	ctx.clearRect(0, 0, canvasWidth, canvasHeight);
	ctx.translate(canvasWidth / 2, canvasHeight / 2);
	ctx.rotate((90 * Math.PI) / 180);
	ctx.translate(-canvasWidth / 2, -canvasHeight / 2);
	ctx.drawImage(
		image,
		canvasWidth / 2 - pictureWidth / 2,
		canvasHeight / 2 - pictureHeight / 2,
		dimensions.width,
		dimensions.height
	);
};

const flip_vertically = (ctx) => {
	ctx.clearRect(0, 0, canvasWidth, canvasHeight);
	ctx.translate(canvasWidth / 2, canvasHeight / 2);
	ctx.scale(-1, 1);
	ctx.translate(-canvasWidth / 2, -canvasHeight / 2);
	ctx.drawImage(
		image,
		canvasWidth / 2 - pictureWidth / 2,
		canvasHeight / 2 - pictureHeight / 2,
		dimensions.width,
		dimensions.height
	);
};

const flip_horizontally = (ctx) => {
	ctx.clearRect(0, 0, canvasWidth, canvasHeight);
	ctx.translate(canvasWidth / 2, canvasHeight / 2);
	ctx.scale(1, -1);
	ctx.translate(-canvasWidth / 2, -canvasHeight / 2);
	ctx.drawImage(
		image,
		canvasWidth / 2 - pictureWidth / 2,
		canvasHeight / 2 - pictureHeight / 2,
		dimensions.width,
		dimensions.height
	);
};

const cropper = (ctx) => {
	console.log('crop');
	windowX = parseInt(resizeContainer.style.left, 10);
	windowY = parseInt(resizeContainer.style.top, 10);
	windowHeight = parseInt(resizeContainer.style.height, 10);
	windowWidth = parseInt(resizeContainer.style.width, 10);

	imageData = ctx.getImageData(
		NW.x + (windowX - NW.x),
		NW.y + (windowY - NW.y),
		windowWidth,
		windowHeight
	);

	crop = document.createElement('canvas');
	crop.width = windowWidth;
	crop.height = windowHeight;
	crop.getContext('2d').putImageData(imageData, 0, 0);
	ctx.clearRect(0, 0, canvasWidth, canvasHeight);
	ctx.putImageData(imageData, NW.x + (windowX - NW.x), NW.y + (windowY - NW.y));

	let imageURL = crop.toDataURL();

	let input = document.getElementById('id_hidden');
	input.value = imageURL;
};

const resizeDragStart = (e) => {
	e.dataTransfer.setData('text/html', e.id);
};

const resizeDrag = (e) => {
	e.stopPropagation();
	offsetX = e.offsetX;
	offsetY = e.offsetY;
	windowX = parseInt(resizeContainer.style.left, 10);
	windowY = parseInt(resizeContainer.style.top, 10);
	width = parseInt(resizeContainer.style.width, 10);
	height = parseInt(resizeContainer.style.height, 10);

	event.dataTransfer.effectAllowed = 'move';

	switch (e.target.id) {
		case 'resize-nw': {
			new_left = windowX + offsetX;
			new_top = windowY + offsetY;
			new_width = width - offsetX;
			new_height = height - offsetY;
			if (new_width > 50) {
				resizeContainer.style.width = width - offsetX + 'px';
				resizeContainer.style.left = windowX + offsetX + 'px';
			}
			if (new_height > 50) {
				resizeContainer.style.height = height - offsetY + 'px';
				resizeContainer.style.top = windowY + offsetY + 'px';
			}
			break;
		}
		case 'resize-ne': {
			new_left = windowX + offsetX;
			new_top = windowY + offsetY;
			new_width = width + offsetX;
			new_height = height - offsetY;
			if (new_width > 50) {
				resizeContainer.style.width = width + offsetX + 'px';
			}
			if (new_height > 50) {
				resizeContainer.style.height = height - offsetY + 'px';
				resizeContainer.style.top = windowY + offsetY + 'px';
			}
			break;
		}
		case 'resize-sw': {
			new_left = windowX + offsetX;
			new_top = windowY + offsetY;
			new_width = width - offsetX;
			new_height = height + offsetY;
			if (new_width > 50) {
				resizeContainer.style.left = windowX + offsetX + 'px';
				resizeContainer.style.width = new_width + 'px';
			}
			if (new_height > 50) {
				resizeContainer.style.height = height + offsetY + 'px';
			}
			break;
		}
		case 'resize-se': {
			new_left = windowX + offsetX;
			new_top = windowY + offsetY;
			// 200 - -50
			new_width = width + offsetX;
			new_height = height + offsetY;
			if (new_width > 50) {
				resizeContainer.style.width = width + offsetX + 'px';
			}
			if (new_height > 50) {
				resizeContainer.style.height = height + offsetY + 'px';
			}
			break;
		}
	}
};

// https://codeburst.io/throttling-and-debouncing-in-javascript-b01cad5c8edf
const throttle = (func, limit) => {
	let inThrottle;
	return function() {
		const args = arguments;
		const context = this;
		if (!inThrottle) {
			func.apply(context, args);
			inThrottle = true;
			setTimeout(() => (inThrottle = false), limit);
		}
	};
};
