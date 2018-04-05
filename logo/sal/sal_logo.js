function preload() {
    // fontHybrid = loadFont('Yahei_Consolas_Hybrid.ttf');
}

function setup(){
    createCanvas(480, 270);
    // createCanvas(256,256);
    // createCanvas(350,380);
    background(20);
    noLoop();
}

function draw() {

    cx = 240;
    cy = 120;
    rmax = 160;
    outerCircle();
    innerCircle();

    // sbTable();
}

function outerCircle() {
    colorMode(RGB,255);
    stroke(165);
    strokeWeight(20);
    ellipse(cx,cy,rmax-1,rmax-1);
}

function innerCircle () {
    ratio = rmax/255;
    noStroke();
    colorMode(HSB,255);
    for (r = 255; r >= 0; r--){
        changeFill();
        ellipse(cx, cy, r*ratio, r*ratio);
    }
}

function changeFill() {
    // Hue, Saturation, Brightness, alpha
    r_inv = invR(r);
    saturation = r;
    brightness = r_inv;

    fill(170, saturation, brightness);
}

function invR(r,max=255){
    r_inv = max - r;
    return r_inv;
}

function sbTable(){
    var px = 60;
    var py = 40;
    background(255);
    colorMode(HSB,255);
    for (var s=0; s<=255; s++) {
        for (var b=0; b<=255; b++){
            stroke(170,s,255-b);
            point(px+s,py+b);
        }
    }
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
}