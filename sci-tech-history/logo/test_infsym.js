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


var lb;

function preload(){
}

function setup(){
    mycreatecanvas = createCanvas(1280,720);
    // mycreatecanvas = createCanvas(1920,1080);
    mycanvas = mycreatecanvas.canvas;
    lb = createGraphics(400, 300);
    background(0);

    plotInfinitySymbol();
    noLoop();

}
function plotInfinitySymbol(){

    pa1 = [20, 10];
    pa2 = [110, 10];
    pc1 = [20, 40];
    pc2 = [60, 60];

    lb.blendMode(ADD);
    // lb.background(200,100);
    lb.colorMode(RGB, 255);
    lb.stroke(0, 255, 0);

    lb.scale(3);
    lb.line(pa1[0], pa1[1], pc1[0], pc1[1]);
    lb.line(pc2[0], pc2[1], pa2[0], pa2[1]);

    lb.strokeWeight(8);
    lb.stroke(155, 155, 155);
    // fill(0, 255, 255);
    lb.noFill();
    lb.bezier(pa1[0], pa1[1], pc1[0], pc1[1], pc2[0], pc2[1], pa2[0], pa2[1]);

    translate(300, 300);
    image(lb, 0, 0, lb.width, lb.height);

    push();
    translate(3*pa2[0], 3*pa2[1]);
    applyMatrix(-1,0,0,1,0,0);
    translate(-3*pa2[0], -3*pa2[1]);
    image(lb, 0, 0, lb.width, lb.height);
    pop();

    push();
    translate(3*pa2[0], 3*pa2[1]);
    applyMatrix(-1,0,0,-1,0,0);
    translate(-3*pa2[0], -3*pa2[1]);
    image(lb, 0, 0, lb.width, lb.height);
    pop();

    push();
    translate(3*pa2[0], 3*pa2[1]);
    applyMatrix(1,0,0,-1,0,0);
    translate(-3*pa2[0], -3*pa2[1]);
    image(lb, 0, 0, lb.width, lb.height);
    pop();

    // filter(BLUR, 1);
    noLoop();
}

function draw(){
}
