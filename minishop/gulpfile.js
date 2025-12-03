var gulp = require('gulp');
sass = require("gulp-sass"),
postcss = require("gulp-postcss");
autoprefixer = require("autoprefixer");
var sourcemaps = require('gulp-sourcemaps');
var browserSync = require('browser-sync').create();
cssbeautify = require('gulp-cssbeautify');
var beautify = require('gulp-beautify');
// const cleanCSS = require('gulp-clean-css');



/*******************  LTR   ******************/


//_______ task for scss folder to css main style 
gulp.task('watch', function() {
    console.log('Command executed successfully compiling SCSS in assets.');
    return gulp.src('static/assets/scss/**/*.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write(''))
        .pipe(gulp.dest('static/assets/css'))
        .pipe(browserSync.reload({
            stream: true
        }))
})

//_______task for dark
gulp.task('dark', function() {
    return gulp.src('static/assets/css/dark.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css'));

})

//_______task for sidemenu
gulp.task('menu', function() {
    return gulp.src('static/assets/css/sidemenu.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css'));

})

//_______task for skins
gulp.task('skins', function() {
    return gulp.src('static/assets/css/skins.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css'));

})

//_______task for boxed
gulp.task('boxed', function() {
    return gulp.src('static/assets/css/boxed.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css'));

})

//_______task for dark-boxed
gulp.task('dark-boxed', function() {
    return gulp.src('static/assets/css/dark-boxed.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css'));

})

//_______task for closed-sidemenu
gulp.task('closed', function() {
    return gulp.src('static/assets/css/closed-sidemenu.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css'));

})

//_______task for sidemenu2
gulp.task('menu2', function() {
    return gulp.src('static/assets/css/sidemenu2.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css'));

})

//_______task for sidemenu3
gulp.task('menu3', function() {
        return gulp.src('static/assets/css/sidemenu3.scss')
            .pipe(sourcemaps.init())
            .pipe(sass())
            .pipe(beautify.css({ indent_size: 4 }))
            // .pipe(cleanCSS({ compatibility: 'ie8' }))
            .pipe(sourcemaps.write('.'))
            .pipe(gulp.dest('static/assets/css'));

    })
    //_______task for sidemenu4
gulp.task('menu4', function() {
    return gulp.src('static/assets/css/sidemenu4.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css'));

})

/*******************  LTR-Beautify  ******************/

//_______ task for beautifying css
gulp.task('beautify', function() {
    return gulp.src('static/assets/css/*.css')
        .pipe(beautify.css({ indent_size: 4 }))
        .pipe(gulp.dest('static/assets/css'));
});



/*******************  RTL  ******************/



//_______ task for scss folder to css main style 
gulp.task('watch-rtl', function() {
    console.log('Command executed successfully compiling SCSS in assets.');
    return gulp.src('static/assets/scss-rtl/**/*.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write(''))
        .pipe(gulp.dest('static/assets/css-rtl'))
        .pipe(browserSync.reload({
            stream: true
        }))
})

//_______task for dark
gulp.task('dark-rtl', function() {
    return gulp.src('static/assets/css-rtl/dark.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css-rtl'));

})

//_______task for sidemenu
gulp.task('menu-rtl', function() {
    return gulp.src('static/assets/css-rtl/sidemenu.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css-rtl'));

})

//_______task for skins
gulp.task('skins-rtl', function() {
    return gulp.src('static/assets/css-rtl/skins.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css-rtl'));

})

//_______task for boxed
gulp.task('boxed-rtl', function() {
    return gulp.src('static/assets/css-rtl/boxed.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css-rtl'));

})

//_______task for dark-boxed
gulp.task('dark-boxed-rtl', function() {
    return gulp.src('static/assets/css-rtl/dark-boxed.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css-rtl'));

})

//_______task for closed-sidemenu
gulp.task('closed-rtl', function() {
    return gulp.src('static/assets/css-rtl/closed-sidemenu.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css-rtl'));

})

//_______task for sidemenu2
gulp.task('menu2-rtl', function() {
    return gulp.src('static/assets/css-rtl/sidemenu2.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css-rtl'));

})

//_______task for sidemenu3
gulp.task('menu3-rtl', function() {
        return gulp.src('static/assets/css-rtl/sidemenu3.scss')
            .pipe(sourcemaps.init())
            .pipe(sass())
            .pipe(beautify.css({ indent_size: 4 }))
            // .pipe(cleanCSS({ compatibility: 'ie8' }))
            .pipe(sourcemaps.write('.'))
            .pipe(gulp.dest('static/assets/css-rtl'));

    })
    //_______task for sidemenu4
gulp.task('menu4-rtl', function() {
    return gulp.src('static/assets/css-rtl/sidemenu4.scss')
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(beautify.css({ indent_size: 4 }))
        // .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('static/assets/css-rtl'));

})


/*******************  RTL-Beautify  ******************/

//_______ task for beautifying css
gulp.task('rtlbeautify', function() {
    return gulp.src('static/assets/css-rtl/*.css')
        .pipe(beautify.css({ indent_size: 4 }))
        .pipe(gulp.dest('static/assets/css-rtl'));
});