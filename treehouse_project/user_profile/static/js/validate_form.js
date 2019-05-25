window.onload = () => {
	document.getElementById('id_avatar').onchange = checkImageSize;
};

const checkImageSize = () => {
	const fileInput = document.getElementById('id_avatar');
	const files = fileInput.files;
	if (files.length > 0) {
		if (files[0].size > 2000000) {
			fileInput.setCustomValidity('Selected image must be smaller than 2mb');
			return;
		}
	}
	fileInput.setCustomValidity('');
};
