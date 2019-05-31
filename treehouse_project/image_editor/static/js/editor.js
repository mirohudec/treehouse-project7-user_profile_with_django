window.onload = () => {
	canvas = document.getElementById('canvas');
	container = document.getElementById('container');
	footer = document.getElementById('buttons');
	resizeContainer = document.getElementById('resize-container');
	container = document.getElementById('container');
	container.style.height = container.clientHeight - footer.clientHeight + 'px';
	upload = document.getElementById('upload');
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

	canvas.width = 500;
	canvas.height = 500;
	canvasWidth = canvas.width;
	canvasHeight = canvas.height;
	ctx = canvas.getContext('2d');
	imageLoader = document.getElementById('input');
	imageLoader.addEventListener('change', (e) => {
		add(e, ctx);
	});
	rotateButton = document.getElementById('rotate_left');
	rotateButton.addEventListener('click', () => {
		rotate_left(ctx);
	});
	rotateButton = document.getElementById('rotate_right');
	rotateButton.addEventListener('click', () => {
		rotate_right(ctx);
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
	removeImage = document.getElementById('remove_image');
	removeImage.addEventListener('click', () => {
		remove_image(ctx);
	});
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

const remove_image = (ctx) => {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    let input = document.getElementById('id_hidden');
	input.value = '';
};

// resizing image to fit in 500 x 500 canvas while keeping its dimensions
const calcNewSize = (srcW, srcH, maxW, maxH) => {
	// don't stretch the image to fit 500 x 500
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

const add = (e, ctx) => {
	let reader = new FileReader();
	reader.onload = (event) => {
		img.onload = () => {
			canvas.style.display = 'block';
			upload.style.display = 'None';
			ctx.clearRect(0, 0, canvasWidth, canvasHeight);
			dimensions = calcNewSize(img.width, img.height, 500, 500);
			image = new Image(dimensions.width, dimensions.height);
			image.src = img.src;
			let input = document.getElementById('id_hidden');
			input.value = image.src;
			resizeContainer.style.display = 'inline-block';
			init(ctx);
		};
		img.src = event.target.result;
	};
	reader.readAsDataURL(e.target.files[0]);
};

const init = (ctx) => {
	pictureWidth = image.width;
	pictureHeight = image.height;
	resizeContainer.style.left =
		canvasWidth / 2 - pictureWidth / 2 + canvas.offsetLeft + 'px';
	resizeContainer.style.top =
		canvasHeight / 2 - pictureHeight / 2 + canvas.offsetTop + 'px';
	resizeContainer.style.width = image.width + 'px';
	resizeContainer.style.height = image.height + 'px';
	containerOffsetX = canvas.clientHeight;
	containerOffsetY = canvas.clientWidth;
	NW = new Point(
		canvasWidth / 2 - pictureWidth / 2 + canvas.offsetLeft,
		canvasHeight / 2 - pictureHeight / 2 + canvas.offsetTop
	);
	SW = new Point(
		canvasWidth / 2 - pictureWidth / 2 + canvas.offsetLeft,
		canvasHeight / 2 - pictureHeight / 2 + img.height + canvas.offsetTop
	);
	NE = new Point(
		canvasWidth / 2 - pictureWidth / 2 + img.width + canvas.offsetLeft,
		canvasHeight / 2 - pictureHeight / 2 + canvas.offsetTop
	);
	SE = new Point(
		canvasWidth / 2 - pictureWidth / 2 + img.width + canvas.offsetLeft,
		canvasHeight / 2 - pictureHeight / 2 + img.height + canvas.offsetTop
	);

	ctx.drawImage(
		image,
		canvasWidth / 2 - pictureWidth / 2,
		canvasHeight / 2 - pictureHeight / 2,
		dimensions.width,
		dimensions.height
	);
};

const rotate_left = (ctx) => {
	ctx.clearRect(0, 0, canvasWidth, canvasHeight);
	ctx.translate(canvasWidth / 2, canvasHeight / 2);
	ctx.rotate(-((90 * Math.PI) / 180));
	ctx.translate(-canvasWidth / 2, -canvasHeight / 2);
	ctx.drawImage(
		image,
		canvasWidth / 2 - pictureWidth / 2,
		canvasHeight / 2 - pictureHeight / 2,
		dimensions.width,
		dimensions.height
	);
};

const rotate_right = (ctx) => {
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
	resizeContLeft = parseInt(resizeContainer.style.left, 10);
	resizeContRight = parseInt(resizeContainer.style.top, 10);
	windowHeight = parseInt(resizeContainer.style.height, 10);
	windowWidth = parseInt(resizeContainer.style.width, 10);

	imageData = ctx.getImageData(
		resizeContLeft - canvas.offsetLeft,
		resizeContRight - canvas.offsetTop,
		windowWidth,
		windowHeight
	);

	crop = document.createElement('canvas');
	crop.width = windowWidth;
	crop.height = windowHeight;
	crop.getContext('2d').putImageData(imageData, 0, 0);
	ctx.clearRect(0, 0, canvasWidth, canvasHeight);
	ctx.putImageData(
		imageData,
		resizeContLeft - canvas.offsetLeft,
		resizeContRight - canvas.offsetTop
	);

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
	resizeContLeft = parseInt(resizeContainer.style.left, 10);
	resizeContRight = parseInt(resizeContainer.style.top, 10);
	width = parseInt(resizeContainer.style.width, 10);
	height = parseInt(resizeContainer.style.height, 10);

	event.dataTransfer.effectAllowed = 'move';

	new_left = resizeContLeft + offsetX;
	new_top = resizeContRight + offsetY;

	switch (e.target.id) {
		case 'resize-nw': {
			new_width = width - offsetX;
			new_height = height - offsetY;
			if (new_width > 50) {
				resizeContainer.style.width = new_width + 'px';
				resizeContainer.style.left = new_left + 'px';
			}
			if (new_height > 50) {
				resizeContainer.style.height = new_height + 'px';
				resizeContainer.style.top = new_top + 'px';
			}
			break;
		}
		case 'resize-ne': {
			new_width = width + offsetX;
			new_height = height - offsetY;
			if (new_width > 50) {
				resizeContainer.style.width = new_width + 'px';
			}
			if (new_height > 50) {
				resizeContainer.style.height = new_height + 'px';
				resizeContainer.style.top = new_top + 'px';
			}
			break;
		}
		case 'resize-sw': {
			new_width = width - offsetX;
			new_height = height + offsetY;
			if (new_width > 50) {
				resizeContainer.style.left = new_left + 'px';
				resizeContainer.style.width = new_width + 'px';
			}
			if (new_height > 50) {
				resizeContainer.style.height = new_height + 'px';
			}
			break;
		}
		case 'resize-se': {
			new_width = width + offsetX;
			new_height = height + offsetY;
			if (new_width > 50) {
				resizeContainer.style.width = new_width + 'px';
			}
			if (new_height > 50) {
				resizeContainer.style.height = new_height + 'px';
			}
			break;
		}
	}
};
