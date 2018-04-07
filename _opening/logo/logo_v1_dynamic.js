pi = Math.PI;
cos = Math.cos;
sin = Math.sin;
floor = Math.floor;

function setup(){
    cnvs = createCanvas(480, 270); // used in logo
    frameRate(30);
    // noLoop();
}

function draw() {
    fc = frameCount;
    console.log(fc);
    calcStage();
    changeBrightnessRatio();
    if (fc<=65){
        drawLogo();
    } else {
        noLoop();
    }
}

function drawLogo() {
    cx = 240;
    cy = 120;
    rmax = 160;
    background(20);
    outerCircle();
    innerCircle();
}

function outerCircle() {
    colorMode(HSB,255);

    stroke(170,10,105*ratio_gray);
    strokeWeight(20);
    ellipse(cx,cy,rmax-1,rmax-1);

    stroke(170,10,165*ratio_silv);
    strokeWeight(13);
    ellipse(cx,cy,rmax-1,rmax-1);
}

function innerCircle () {
    ratio = rmax/255;
    noStroke();
    colorMode(HSB,255);
    for (var r = 255; r >= 0; r--){
        changeFill(r);
        ellipse(cx, cy, r*ratio, r*ratio);
    }

    function changeFill(r) {
        var k = 400;
        var theta = (255-r)/255*(pi/2);
        var sat = floor(k*cos(theta));
        var bri = floor(k*sin(theta));

        if (r>=130){
            fill(170, sat, (bri-70)*ratio_black); // black
        } else if (r>=30) {
            fill(170, sat, bri*ratio_blue); // blue
        } else {
            fill(170, sat-6, (bri-70)*ratio_white); // white
        }
    }
}

function calcStage() {
    if (fc<=30) {
        stage = 1;
    } else if (fc<=60){
        stage = 2;
    } else if (fc<=90) {
        stage = 3;
    } else {
        stage = 4;
    }
}

function changeBrightnessRatio() {
    if (fc<=30){
        ratio_gray = fc/30;
        ratio_silv = fc/30;
    } else {
        ratio_gray = 1;
        ratio_silv = 1;
    }

    var bgn_white = 20;
    if (fc<=bgn_white){
        ratio_white = 0;
    } else if (fc<=bgn_white+30){
        ratio_white = (fc-bgn_white)/30;
    } else {
        ratio_white = 1;
    }

    var bgn_black = 25;
    if (fc<=bgn_black){
        ratio_black = 0;
        ratio_blue = 0;
    } else if (fc <=bgn_black+30) {
        ratio_black = (fc-bgn_black)/30;
        ratio_blue = (fc-bgn_black)/30;
    } else {
        ratio_black = 1;
        ratio_blue = 1;
    }
    
}