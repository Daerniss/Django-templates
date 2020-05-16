function throttle (func, wait, options) {
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

const headerThrottling = throttle(headerHandler, 200);

// HEADER
const classes = {
	pinned   : 'header__pin',
	unpinned : 'header__unpin',
	top      : 'header__top'
};
document.addEventListener('scroll', headerThrottling);
let lastKnownScrollY = 0;
const header = document.querySelector('.header');

function headerHandler (e) {
	let currentY = window.pageYOffset;

	if (currentY == 0) {
		header.classList.remove(classes.pinned);
		header.classList.remove(classes.unpinned);
		document.querySelector('.header').classList.add(classes.top);
	} else if (currentY > lastKnownScrollY) {
		header.classList.remove(classes.pinned);
		header.classList.add(classes.unpinned);
		document.querySelector('.header').classList.remove(classes.top);
	} else if (currentY < lastKnownScrollY) {
		header.classList.remove(classes.unpinned);
		header.classList.add(classes.pinned);
		document.querySelector('.header').classList.remove(classes.top);
	}

	lastKnownScrollY = currentY;
}

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
document.querySelector('.questions').addEventListener('click', (e) => {
	const item = e.target.closest('.questions__item');
	const content = item.lastElementChild;
	item.classList.toggle('questions__item--active');
	content.classList.toggle('questions__content--active');
});
