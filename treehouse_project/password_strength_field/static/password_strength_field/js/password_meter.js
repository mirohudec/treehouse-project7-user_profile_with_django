(function() {
	let meterField;
	function StrengthMeterField(passwordInput) {
		meterField = document.getElementById('meter-value');
		meterField.clientWidth = 200;
		new_password = document.getElementById(passwordInput.id);
		new_password.addEventListener('input', (e) => {
			pw_length = e.target.value.length;
			if (pw_length < 14) {
				meterField.className = 'color_super_weak';
				meterField.style.width = '20%';
			} else if (pw_length < 16) {
				meterField.className = 'color_weak';
				meterField.style.width = '20%';
			} else if (pw_length < 18) {
				meterField.className = 'color_medium';
				meterField.style.width = '20%';
			} else if (pw_length < 20) {
				meterField.className = 'color_good';
				meterField.style.width = '20%';
			} else if (pw_length < 22) {
				meterField.className = 'color_strong';
			}
			if (pw_length < 23) {
				meterField.style.width = pw_length * 4.54 + '%';
			}
		});
	}

	document.addEventListener('DOMContentLoaded', function(e) {
		[].forEach.call(
			document.querySelectorAll('[strength-value]'),
			StrengthMeterField
		);
	});
})();
