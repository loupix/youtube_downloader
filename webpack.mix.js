const mix = require('laravel-mix');

let staticPath = 'app/static/build'
let resourcesPath = 'app/resources'

mix.setResourceRoot('app/ressources') // setResroucesRoots add prefix to url() in scss on example: from /images/close.svg to /static/images/close.svg

mix.setPublicPath('app/static/build') // Path where mix-manifest.json is created


// if you don't need browser-sync feature you can remove this lines
if (process.argv.includes('--browser-sync')) {
  mix.browserSync('localhost:8000')
}

// Now you can use full mix api

mix.js([`${resourcesPath}/js/appConfig.js`, 
    `${resourcesPath}/js/homeCtrl.js`, `${resourcesPath}/js/topCtrl.js`, `${resourcesPath}/js/videoCtrl.js`,
    `${resourcesPath}/js/loginCtrl.js`, `${resourcesPath}/js/registerCtrl.js`,
    `${resourcesPath}/js/historyCtrl.js`, `${resourcesPath}/js/statistiqueCtrl.js`,
    `${resourcesPath}/js/facialCtrl.js`, `${resourcesPath}/js/vocalCtrl.js`,],
    `${staticPath}/app.js`);


mix.postCss(`${resourcesPath}/css/style.css`, `${staticPath}/app.css`);

