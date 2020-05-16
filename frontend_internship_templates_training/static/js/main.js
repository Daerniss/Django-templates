function throttle(func, wait, options) {
	var context, args, result;
	var timeout = null;
	var previous = 0;
	if (!options) options = {};
	var later = function () {
		previous = options.leading === false ? 0 : Date.now();
		timeout = null;
		result = func.apply(context, args);
		if (!timeout) context = args = null;
	};
	return function () {
		var now = Date.now();
		if (!previous && options.leading === false) previous = now;
		var remaining = wait - (now - previous);
		context = this;
		args = arguments;
		if (remaining <= 0 || remaining > wait) {
			if (timeout) {
				clearTimeout(timeout);
				timeout = null;
			}
			previous = now;
			result = func.apply(context, args);
			if (!timeout) context = args = null;
		} else if (!timeout && options.trailing !== false) {
			timeout = setTimeout(later, remaining);
		}
		return result;
	};
}

// HEADER
(function () {
	const header = document.querySelector('.header');
	let lastKnownScrollY = 0;

	const classes = {
		pinned: 'header__pin',
		unpinned: 'header__unpin',
		top: 'header__top'
	};

	document.addEventListener('scroll', throttle(headerHandler, 500));

	function headerHandler(e) {
		let currentY = window.pageYOffset;
		console.log(currentY);

		if (currentY === 0) {
			header.classList.remove(classes.pinned);
			header.classList.remove(classes.unpinned);
			header.classList.add(classes.top);
		} else if (currentY > lastKnownScrollY) {
			header.classList.remove(classes.pinned);
			header.classList.remove(classes.top);
			header.classList.add(classes.unpinned);
		} else if (currentY < lastKnownScrollY) {
			header.classList.remove(classes.unpinned);
			header.classList.remove(classes.top);
			header.classList.add(classes.pinned);
		}

		lastKnownScrollY = currentY;
	}
}())


document.querySelector('#menuToggle').addEventListener('change', function (e) {
	const check = document.querySelector('#menuToggle');
	const html = document.querySelector('html');

	if (check.checked) {
		html.style.overflow = 'hidden';
	} else {
		html.style.overflow = 'visible';
	}
});

///////////////////// FAQ
if (document.querySelector('.questions')) {
	document.querySelector('.questions').addEventListener('click', (e) => {
		const item = e.target.closest('.questions__item');
		const header = e.target.closest('.questions__header');

		if (header) {
			item.classList.toggle('questions__item--active');
		}
	});
}

// CONTACT US FORM
(function () {
	const contactUs = document.querySelector('#contactUs-form');

	if (contactUs) {
		contactUs.addEventListener('submit', async (e) => {
			e.preventDefault();
			const fields = document.querySelectorAll('.form__group');

			// Clear errors
			[...fields.values()].forEach(field => {
				field.children[2].textContent = '';
			})

			let response = await fetch('', {
				method: 'POST',
				body: new FormData(contactUs)
			});

			// If form is incorrect: display error messages
			// Else: display success message and redirect
			if (response.status !== 200) {
				let result = await response.json();

				// Check for errors
				Object.entries(result).forEach((item) => {
					[...fields.values()].forEach(field => {
						if (field.classList.contains(`form__group--${item[0]}`)) {
							field.children[2].textContent = item[1];
						}
					})
				});
			} else {
				document.querySelector('.modal').classList.add('modal__active');
				setTimeout(function () {
					window.location.href = '/';
				}, 2000);
			}
		});
	}
}())