/* 

This file requires:

********** Online **********
- jquery.min.js
- p5.min.js
- python-format.js
- object-watch.js

********** Custom **********
- assistant-function.js
- Block.js

*/

let socket = io();
let videodata;
let blockarr = [];
let sortedarr =[];
let namearr = [];
let rgb =[];
let rownum, colnum;

let block_x = 100;
let block_y_bias = 80;
let block_h = 30;
let block_gap = 10;
let block_w_max = 680;
let block_w_bias = 1;


function preload(){
    // | 累计播放量 | 动画 | 番剧 | 国创 | 音乐 | 舞蹈 | 游戏 | 科技 | 生活 | 鬼畜 | 时尚 | 广告 | 娱乐 | 影视 | 放映厅 |
    // |      0     |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |  10  |  11  |  12  |  13  |   14   |

    videodata = loadTable('./videoviews.csv','csv');
}

function setup(){
    mycreatecanvas = createCanvas(1280,720);
    // mycreatecanvas = createCanvas(1920,1080);
    mycanvas = mycreatecanvas.canvas;
    background(0);
    // frameRate(30);

    initBlocks();

    // noLoop();
}

function draw() {
    fc = frameCount;

    if (fc >= rownum-1){
        noLoop();
    }

    scale(window.width/1280, window.height/720);

    drawMain();
}


function drawMain(){
    background(0);
    dispFrameRate();
    row = videodata.getRow(fc); // fc start from 1
    dispDay();
    sortArray();
    for (let i=0; i<colnum-1;i++){
        blockarr[i].move();
        blockarr[i].disp();
    }
    // drawAxis();
    drawPieChart();
    // saveFrame();
}


function initBlocks() {
    row = videodata.getRow(1);
    colnum = videodata.getColumnCount();
    rownum = videodata.getRowCount();
    namearr = videodata.getRow(0);
    rgbarr = [ [0.5, 0.5,  1 ], [0.5, 0.5,  1 ], [0.5, 0.5,  1 ],
               [ 1 ,  1 ,  0 ], [ 1 , 0.5,  0 ], [ 1 ,  0 ,  0 ],
               [ 0 , 0.5,  1 ], [ 0 , 0.5,  0 ], [0.5,  1 ,  1 ],
               [ 1 , 0.5,  1 ], [ 1 , 0.5,  1 ], [ 1 , 0.5,  1 ],
               [ 1 , 0.5,  1 ], [ 1 , 0.5,  1 ]];

    for (let i=0; i<colnum-1; i++){
        let block = new Block(i,namearr.getString(i+1));
        // console.log(block.name);
        block.x = block_x;
        block.y = (block_h + block_gap)*i + block_y_bias;
        block.w = 100;
        block.h = block_h;
        // block.hue = i/colnum*255;
        [block.r, block.g, block.b] = [255*rgbarr[i][0], 255*rgbarr[i][1], 255*rgbarr[i][2]];
        blockarr[i] = block;
    }

    // // To make the first frame ordered
    sortArray();
    for (let j=0; j<26; j++) {
        for (let i=0; i<colnum-1; i++){
            blockarr[i].move();
        }
    }
    for (let i=0; i<colnum-1; i++){
        blockarr[i].disp();
    }

}

function drawPieChart(){
    let totalnum=0;
    for (let i=0; i<colnum-1; i++){
        totalnum += blockarr[i].value;
    }
    let ratio = [];
    for (let i=0; i<colnum-1; i++){
        // I add one to the value to avoid angle from 0 to 0
        // Because arc(x,y,w,h,0,0,PIE) will fill the whole pie chart.
        // I add 100 to the totalnum to avoid sum of angle exceeds 2*PI.
        ratio[i] = (blockarr[i].value+1)/(totalnum+100);
    }

    let ang_bgn = -Math.PI*(1/2);
    let ang_end;
    let pie_r = 100;
    let pie_d = 2 * pie_r;
    let [pie_x, pie_y] = [980, 520];
    let angs = [];
    for (let i=0; i<colnum-1; i++){
        block = blockarr[i];
        ang_end = ang_bgn + 2*Math.PI*ratio[i];
        colorMode(RGB,255);
        stroke(255);
        fill(block.r, block.g, block.b);
        arc(pie_x, pie_y, pie_d, pie_d, ang_bgn,ang_end,PIE);

        let ang_half = (ang_bgn+ang_end)/2;
        angs[i] = ang_half;
        ang_bgn = ang_end;
    }

    // Add labels
    let vtx = [];
    let orients = [];

    for (let i=0; i<colnum-1; i++){
        let ang = angs[i];
        let [dx,dy] = [pie_r*Math.cos(ang), pie_r*Math.sin(ang)];
        let [x1,y1] = [pie_x+dx, pie_y+dy];
        let [x2,y2] = [pie_x+1.3*dx, pie_y+1.3*dy];

        let orient;
        if (ang<Math.PI/2){
            orient = 1;
        } else {
            orient = -1;
        }

        // // Improve margin of labels
        // if (i>=8) {
        //     for (let j=0; j<i; j++){
        //         let diff_x = x2 - vtx[j].x2;
        //         let diff_y = y2 - vtx[j].y2;
        //         while (Math.abs(diff_x)<40 && Math.abs(diff_y)<40){
        //             x2 = (x2-pie_x)*1.1 + pie_x;
        //             y2 = (y2-pie_y)*1.1 + pie_y;
        //             diff_x = x2 - vtx[j].x2;
        //             diff_y = y2 - vtx[j].y2;
        //         }
        //     }
        // }

        let [x3,y3] = [x2+30*orient, y2];

        let tmp = {};
        [tmp.x1,tmp.y1] = [x1,y1];
        [tmp.x2,tmp.y2] = [x2,y2];
        [tmp.x3,tmp.y3] = [x3,y3];
        vtx[i] = tmp;
        orients[i] = orient;
    }


    // for (let i=0; i<colnum-1; i++){
    for (let i=colnum-2; i>=0; i--){
        block = blockarr[i];
        let orient = orients[i];
        noFill();
        colorMode(RGB,255);
        strokeWeight(1);
        stroke(block.r,block.g,block.b);

        let [x1,y1] = [vtx[i].x1, vtx[i].y1];
        let [x2,y2] = [vtx[i].x2, vtx[i].y2];
        let [x3,y3] = [vtx[i].x3, vtx[i].y3];

        beginShape();
        vertex(x1,y1);
        vertex(x2,y2);
        vertex(x3,y3);
        endShape();

        noStroke();
        fill(block.r,block.g,block.b);
        // console.log(orient);
        textAlign((orient>0)?LEFT:RIGHT,CENTER);
        // textSize(14);
        text(block.name,x3+orient*5,y3);
        let name_width = textWidth(block.name);
        text(xround(ratio[i]*100,2)+'% ',x3+orient*(10+name_width),y3)

    }
}


function drawBonusScene(){
    
}

function drawAxis(){
    let block_max = blockarr[sortedarr[0].id];
    let val_max = block_max.value;
    let num_str = val_max.toString();
    let [num_len, digits, max_ceil] = calcMaxCeil(val_max);

    let ax_str = format('{}.{}x10^{}', digits[0], digits[1], num_len-1);
    let ax_str2 = num2unit(val_max);
    // let axunit_x = max_ceil/val_max * block_w_max + block_w_bias;
    colorMode(RGB,255);
    noStroke();
    fill(block_max.r,block_max.g,block_max.b);
    textAlign(RIGHT);
    var m = text(ax_str, block_x + block_w_max + block_w_bias + 75, 50);
    // console.log(m);
    text(ax_str2, block_x + block_w_max + block_w_bias + 75, 20);
}

function saveFrame(title, count){
    let url = mycanvas.toDataURL('image/png');
    socket.emit('saveFrame', url, title, count);
}

function dispFrameRate(){
    let ratestr = format('{:>02d} FPS',floor(frameRate()));
    let cntstr = format('# {:>05d}',frameCount);
    colorMode(RGB,255);
    stroke(0,255,0);
    // noStroke();
    fill(0,255,0);
    textSize(15);
    text(ratestr,100,50);
    text(cntstr,200,50);
}

function dispDay(){
    let day = row.getString(0);
    colorMode(RGB,255);
    stroke(0,255,0);
    // noStroke();
    fill(0,255,0);
    textSize(15);
    text(day,350,50);
}