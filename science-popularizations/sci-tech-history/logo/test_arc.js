/* 

This file requires:

********** Online **********
- jquery.min.js
- p5.min.js
- math.min.js
- python-format.js
- object-watch.js

********** Custom **********

*/

pi = Math.PI


function preload(){
}

function setup(){
    mycreatecanvas = createCanvas(1280,720);
    // mycreatecanvas = createCanvas(1920,1080);
    mycanvas = mycreatecanvas.canvas;
    background(0);

    infsym = createGraphics(400, 400);
    infsym.ellipseMode(RADIUS);
    // infsym.background(120, 30);
    infsym.noFill();
    infsym.strokeWeight(10);
    infsym.stroke(0, 255, 255);
    infsym.point(100, 50);
    infsym.arc(80, 80, 40, 40, 0.5*pi, 1.5*pi);
    recbg = createGraphics(80, 80);
    recbg.colorMode(RGB, 255);
    recbg.background(255, 0, 0);
    recbg.filter(BLUR, 3);
    noLoop();

}

function draw() {
    console.log(frameRate());
    image(infsym, 40, 40, 400, 400);

    push();
    translate(infsym.width/2+40, infsym.height/2+40);
    // rotate(pi);
    applyMatrix(-1, 0, 0, 1, 0, 0);
    translate(-240, -240);
    image(infsym, 40, 40, 400, 400);
    
    infsym_blur = infsym.get();
    infsym_blur.filter(BLUR, 8);
    image(infsym_blur, 40, 40, 400, 400);
    pop();
    
    image(infsym, 90, 40, 400, 400);

    // (imgmasked = infsym.get()).mask(recbg.get());
    (imgmasked = recbg.get()).mask(infsym.get());
    image(imgmasked, 260, 60, infsym.width, infsym.height);
}

