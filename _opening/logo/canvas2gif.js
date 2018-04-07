function setup(){
    mycanvas_parent = createCanvas(480,270);
    mycanvas_parent.parent('mycanvasdiv');
    mycanvas = mycanvas_parent.canvas;
    mycontext = mycanvas.getContext('2d');
    background(20);
    setEncoder();
    // noLoop();
}

function draw(){
    fc = frameCount;
    console.log(fc);
    if (fc<=30){
        circ();
        myencoder.addFrame(mycontext);
    } else {
        noLoop();
        myencoder.finish();
        document.getElementById('myimg').src = 'data:image/gif;base64,'+encode64(myencoder.stream().getData());
    }
}

function circ(){
    colorMode(HSB);
    fill(fc*2,255,255);
    ellipse(220,120,80,80);
}

function setEncoder(){
    myencoder = new GIFEncoder();
    myencoder.setRepeat(0);
    myencoder.setDelay(100);
    console.log(myencoder.start());
}