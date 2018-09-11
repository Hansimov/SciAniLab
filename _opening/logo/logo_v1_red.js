pi = Math.PI;
cos = Math.cos;
sin = Math.sin;
floor = Math.floor;

main_hue = 0;

function setup(){
    cnvs = createCanvas(480, 270); // used in logo
    noLoop();
}

function draw() {
    cx = 240;
    cy = 120;
    rmax = 160;
    drawLogo();
    // drawSBTable();
    // drawGrayTable();
}

function drawLogo() {
    background(20);
    outerCircle();
    innerCircle();
}

function outerCircle() {
    colorMode(HSB,255);

    stroke(main_hue,10,105);
    strokeWeight(20);
    ellipse(cx,cy,rmax-1,rmax-1);
    stroke(main_hue,10,165);
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
            fill(main_hue, sat, bri-70);
        } else if (r>=25) {
            fill(main_hue, sat, bri);
        } else {
            // fill(main_hue, sat-6, bri);
            fill(45, sat, 255)
        }
    }
}

function invR(r,max=255){
    var r_inv = max - r;
    return r_inv;
}

function drawSBTable(){
    createCanvas(350,380); // used in sbtable
    var px = 60;
    var py = 40;
    colorMode(HSB,255);
    background(255);

    for (var s=0; s<=255; s++) {
        for (var b=0; b<=255; b++){
            stroke(main_hue,s,255-b);
            point(px+s,py+b);
        }
    }
    addText();

    function addText(){
        // textFont('Monospaced');
        textAlign(RIGHT,CENTER);
        text('255', px-10,      py);
        text('0',   px-10,      py+256);
        text('亮',px-35,py+120);
        text('度',px-35,py+140);
        textAlign(CENTER);
        text('0',   px,     py+270);
        text('255', px+256, py+270);
        text('饱 和 度',px+128,py+295);
        text('Hue = ' + main_hue.toString(), px+128, py+320);
    }
}

function drawGrayTable(){
    createCanvas(350,380); // used in graytable
    var px = 60;
    var py = 40;
    colorMode(RGB,255);
    background(255);

    for (var row=0; row<=255; row++){
        for (var col=0; col<=50; col++){
            stroke(row);
            point(px+row,py+col);
        }
    }
}