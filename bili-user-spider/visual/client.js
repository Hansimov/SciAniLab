let socket = io();
let userdatastr;
let userdata = [];

sin = Math.sin;
cos = Math.cos;
floor = Math.floor;

function preload(){
    userdatastr = loadStrings('./user.txt');
}

function setup(){
    parseDataFile();
    mycanvas = createCanvas(1280,720);
    mycanvas = mycanvas.canvas;
    background(0);
    frameRate(10);
    // noLoop();
}

function draw() {
    if (frameCount>=userdata.length-10){
        noLoop();
    }
    
    plotCurve();
    dispFrameRate();
}


function parseDataFile(){
    for (let i=0; i < userdatastr.length; i++){
        let arr = userdatastr[i].split(' ');
        userdata[i] = {};
        userdata[i].day = arr[0];
        userdata[i].mid = arr[1];
        userdata[i].name = arr[5];
    }
}

function plotCurve(){
    background(0);
    for (let i=0; i<10; i++){
        // point()
        colorMode(RGB,255);
        stroke(255,255,25*i);
        fill(255,255,25*i);
        textSize(15);
        text(userdata[i+frameCount].day,100, 200+i*30);
        text(userdata[i+frameCount].name,200, 200+i*30);

        // console.log(userdata[frameCount].name);
    }
}

function plotYAxis(){

}

function plotXAxis(){

}

function plotLeadingPoint(){

}



function data2point(){

}

function saveFrame(){
    let dataurl = mycanvas.toDataURL('image/png', 1);
    socket.emit('dataurl', dataurl, frameCount);
}

function dispFrameRate(){
    let ratestr = floor(frameRate()).toString() + ' FPS';

    stroke(255,0,0);
    textSize(15);
    text(ratestr,100,50);
    text(frameCount,150,50);
    // console.log(ratestr);
}

