"use strict";

const gulp = require("gulp");
const path = require("path");
const data = require("gulp-data");
const pug = require("gulp-pug");
const prefix = require("gulp-autoprefixer");
const sass = require("gulp-sass");
const browserSync = require("browser-sync");

/*
 * Directories here
 */
const paths = {
  dist: "./dist/",
  css: "./dist/css/",
  images: "./dist/images/",
  jsfiles: "./dist/js/",
  sass: "./src/scss/",
  data: "./src/_data/"
};

/**
 * Compile .pug files and pass in data from json file
 * matching file name. index.pug - index.pug.json
 */
gulp.task("pug", () => {
  return gulp.src("./src/pug/*.pug")
    // .pipe(data((file) => require(`${paths.data}${path.basename(file.path)}.json`)))
    .pipe(pug())
    .on("error", (err) => { console.log(err.message); })
    .pipe(gulp.dest(paths.dist));
});

/**
 * Trigger browser reload.
 */
gulp.task("bs:reload", (done) => {
  browserSync.reload();
  done();
});

/**
 * Launch BrowserSync.
 */
gulp.task("bs", () => {
  return browserSync({
    server: {baseDir: paths.dist},
    notify: false
  });
});

/**
 * Compile .scss files into dist css directory With autoprefixer no
 * need for vendor prefixes then live reload the browser.
 */
gulp.task("sass", () => {
  const sassOptions = {
    includePaths: [paths.sass],
    outputStyle: "compressed"
  };

  return gulp.src(paths.sass + "*.scss")
    .pipe(sass(sassOptions))
    .on("error", sass.logError)
    .pipe(prefix(["last 15 versions", "> 1%", "ie 8", "ie 7"], {cascade: true}))
    .pipe(gulp.dest(paths.css))
    .pipe(browserSync.stream());
});

/** Copy images to dist **/
gulp.task("copy:images", () => {
  return gulp.src("./src/images/**/*.{jpg,gif,png,svg}")
    .pipe(gulp.dest(paths.images));
});

/** Copy js to dist **/
gulp.task("copy:js", () => {
  return gulp.src("./src/js/**/*")
    .pipe(gulp.dest(paths.jsfiles));
});

/**
 * Watch scss files for changes & recompile.
 * Watch .pug files run pug task then reload browser.
 */
gulp.task("watch", () => {
  gulp.watch(paths.sass + "**/*.scss", gulp.task("sass"));
  gulp.watch("./src/**/*.pug", gulp.series("pug", "bs:reload"));
});

// Main tasks
gulp.task("build", gulp.series("sass", "pug", "copy:images", "copy:js"));
gulp.task("default", gulp.series("build", gulp.parallel("bs", "watch")));
