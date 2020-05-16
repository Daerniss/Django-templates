const gulp = require('gulp');
const browserSync = require('browser-sync').create();
const watch = require('gulp-watch');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');
const sourcemaps = require('gulp-sourcemaps');
const notify = require('gulp-notify');
const plumber = require('gulp-plumber');
const imagemin = require('gulp-imagemin');

gulp.task('scss', function () {
	return gulp
		.src('./frontend_internship_templates_training/src/scss/main.scss')
		.pipe(
			plumber({
				errorHandler: notify.onError(function (err) {
					return {
						title: 'Styles',
						sound: false,
						message: err.message
					};
				})
			})
		)
		.pipe(sourcemaps.init())
		.pipe(sass())
		.pipe(
			autoprefixer({
				overrideBrowserslist: [
					'last 2 versions'
				]
			})
		)
		.pipe(sourcemaps.write())
		.pipe(gulp.dest('./frontend_internship_templates_training/static/css/'));
});

gulp.task('copy:img', function (callback) {
	return gulp
		.src('./frontend_internship_templates_training/src/img/**/*.*')
		.pipe(imagemin())
		.pipe(gulp.dest('./frontend_internship_templates_training/static/img/'));
});

gulp.task('copy:js', function () {
	return gulp
		.src('./frontend_internship_templates_training/src/js/**/*.js')
		.pipe(gulp.dest('./frontend_internship_templates_training/static/js/'));
});

gulp.task('copy:fonts', function (callback) {
	return gulp
		.src('./frontend_internship_templates_training/src/fonts/**/*.*')
		.pipe(gulp.dest('./frontend_internship_templates_training/static/fonts/'));
});

gulp.task('watch', function () {
	watch(
		[
			'./frontend_internship_templates_training/static/js/**/*.*',
			'./frontend_internship_templates_training/static/img/**/*.*'
		],
		gulp.parallel(browserSync.reload)
	);
	watch('./frontend_internship_templates_training/*.html', gulp.parallel(browserSync.reload));

	watch('./frontend_internship_templates_training/src/scss/**/*.scss', gulp.parallel('scss'));

	watch('./frontend_internship_templates_training/src/img/**/*.*', gulp.parallel('copy:img'));
	watch('./frontend_internship_templates_training/src/js/**/*.*', gulp.parallel('copy:js'));
	watch('./frontend_internship_templates_training/src/fonts/**/*.*', gulp.parallel('copy:fonts'));
});

gulp.task(
	'default',
	gulp.series(gulp.parallel('scss', 'copy:img', 'copy:js', 'copy:fonts'), gulp.parallel('watch'))
);
