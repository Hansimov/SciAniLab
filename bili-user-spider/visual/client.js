let img;

socket = io();

// function preload(){
//     img = loadImage("./images/hal9000.jpg");
// }


function setup(){
    mycanvas = createCanvas(1280,720);
    mycanvas = mycanvas.canvas;
    background(0);
    frameRate(20);
    // noLoop();
}

function draw() {
    if (frameCount>=20){
        noLoop();
    }
    fill(200,300,300);
    ellipse(100,20,frameCount,frameCount);
    // image(img, 0, img.height/2, img.width/2, img.height/2);
    var url = mycanvas.toDataURL('image/png', 0.1);
    socket.emit('dataurl',url,frameCount);
}


