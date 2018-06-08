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
    lb = createGraphics(1280, 720);
    background(0);
    noLoop();
}

function draw(){
    lb.scale(3);
    lb.blendMode(ADD);
    lb.background(200,100);
    lb.translate(100, 100);
    lb.colorMode(RGB, 255);
    lb.stroke(0, 255, 0);
    lb.strokeWeight(5);

    pa1 = [0, 10];
    pa2 = [100, 10];
    pc1 = [0, 30];
    pc2 = [40, 60];

    lb.line(pa1[0], pa1[1], pc1[0], pc1[1]);
    lb.line(pc2[0], pc2[1], pa2[0], pa2[1]);
    lb.stroke(255, 0, 0);
    // fill(0, 255, 255);
    lb.noFill();
    lb.bezier(pa1[0], pa1[1], pc1[0], pc1[1], pc2[0], pc2[1], pa2[0], pa2[1]);
    image(lb, 0, 0, lb.width, lb.height);

    push();
    translate(lb.width+pa2[0], lb.height+pa2[1]);
    applyMatrix(-1,0,0,-1,0,0);
    // translate(-(lb.width+pa2[0]), -(lb.height+pa2[1]));
    image(lb, 0, 0, lb.width, lb.height);
    pop();

}
