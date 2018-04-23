/* 

This file requires:

********** Online **********
- jquery.min.js
- p5.min.js
- math.min.js
- python-format.js
- object-watch.js

********** Custom **********
- assistant-function.js
- Classes.js

*/

try {
    let socket = io();
} catch(e) {
    console.log(e);
}

let videodata;
let blockarr = [];
let sortedarr =[];
let namearr = [];
let rownum, colnum;

let block_x = 100;
let block_y_bias = 210;
let block_h = 25;
let block_gap = 8;
let block_w_max = 630;
let block_w_bias = 1;

let progress_color = [];

function preload(){
    // | 累计播放量 | 动画 | 番剧 | 国创 | 音乐 | 舞蹈 | 游戏 | 科技 | 生活 | 鬼畜 | 时尚 | 广告 | 娱乐 | 影视 | 放映厅 |
    // |      0     |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |  10  |  11  |  12  |  13  |   14   |
    try {
        videodata = loadTable('./videoviews.csv','csv');
    } catch(e) {
        console.log(e);
    }
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
    // saveFrame('whole',fc);
}


function drawMain(){
    background(0);
    // dispFrameRate();
    row = videodata.getRow(fc); // fc start from 1
    // dispDay();
    sortArray();

    drawAxis();
    for (let i=0; i<colnum-1;i++){
        blockarr[i].move();
        blockarr[i].disp();
    }
    drawPieChart();
    drawProgress('h');
    // saveFrame();
}


function initBlocks(initframe=1) {
    row = videodata.getRow(initframe);
    colnum = videodata.getColumnCount();
    rownum = videodata.getRowCount();
    namearr = videodata.getRow(0);
    let rgbarr = [ [0.5, 0.5,  1 ], [0.5, 0.5,  1 ], [0.5, 0.5,  1 ],
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


function drawBonusScene(){
    
}



function drawProgress(orient){
    let block_max = blockarr[sortedarr[0].id];
    let today_color = color(block_max.r, block_max.g, block_max.b);
    let progress_x, progress_y, progress_w, progress_h;
    progress_color[fc-1] = today_color;

    if (orient == 'v') {        // Vertical
        progress_x = 1050;
        progress_y = 300 - 200/3200*fc;
        progress_w = 25;
        progress_h = 1;
    } else if (orient == 'h'){  // Horizontal
        progress_x = block_x + fc/(rownum-1)*block_w_max;
        progress_y = block_y_bias - 130;
        progress_w = Math.max(block_w_max/(rownum-1),1);
        progress_h = block_h - 10;
    }

    push();
    colorMode(RGB,255);
    noStroke();

    // Draw progress bar
    for (let i = 1; i<=fc; i++){
        fill(progress_color[i-1]);
        if (orient=='v'){
            let progress_y_tmp = 300 - 200/3200 * i;
            rect(progress_x, progress_y_tmp , progress_w, progress_h);
        } else if (orient=='h'){
            let progress_x_tmp = block_x + i/(rownum-1)*block_w_max;
            rect(progress_x_tmp, progress_y , progress_w, progress_h);
        }
    }
    // Draw border of bar
    push();
    stroke(128,128,128,128);
    noFill();
    // fill(255,0,0,255);
    strokeWeight(2);
    rect(block_x-1, progress_y, block_w_max, progress_h);
    pop();

    // Draw NO.1 color
    push();
    rectMode(CENTER);
    fill(today_color);
    rect(block_x-30,progress_y+progress_h/2, 2*progress_h, 2*progress_h);
    pop();


    // Disp day
    let day = row.getString(0);
    if (orient == 'v'){
        textAlign(LEFT,CENTER);
        textSize(16);
        text(day, progress_x+progress_w+25, progress_y);

        noFill();
        stroke(today_color);
        line(progress_x+progress_w+5, progress_y, progress_x+progress_w+20, progress_y);
    } else if (orient=='h'){
        textAlign(CENTER);
        textSize(16);
        text(day, progress_x, progress_y-30);

        noFill();
        stroke(today_color);
        line(progress_x, progress_y-5, progress_x, progress_y-25);
    }

    pop();
}

function drawPieChart(){

    // Calc ratios
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

    // Draw arcs
    let ang_bgn = -Math.PI*(1/2);
    let ang_end;
    let pie_r = 100;
    let pie_d = 2 * pie_r;
    let [pie_x, pie_y] = [1050, 560];
    let angs = [];
    colorMode(RGB,255);
    for (let i=0; i<colnum-1; i++){
        block = blockarr[i];
        ang_end = ang_bgn + 2*Math.PI*ratio[i];
        stroke(168,168,168,255);
        fill(block.r, block.g, block.b);
        arc(pie_x, pie_y, pie_d, pie_d, ang_bgn,ang_end,PIE);

        let ang_half = (ang_bgn+ang_end)/2;
        angs[i] = ang_half;
        ang_bgn = ang_end;
    }

    let circ_d = pie_d * 2/3;
    push();
    noStroke();
    fill(0,0,0);
    ellipse(pie_x, pie_y, circ_d, circ_d);
    pop();

    // Improve margin of labels
    let vtx = [];
    let orients = [];
    let rscales = [];
    for (let i=0; i<colnum-1; i++){
        let ang = angs[i];
        let orient;
        if (ang<Math.PI/2){
            orient = 1;
        } else {
            orient = -1;
        }

        let [dx,dy] = [pie_r*Math.cos(ang), pie_r*Math.sin(ang)];
        let [x1,y1] = [pie_x+dx, pie_y+dy];
    // | 动画 | 番剧 | 国创 | 音乐 | 舞蹈 | 游戏 | 科技 | 生活 | 鬼畜 | 时尚 | 广告 | 娱乐 | 影视 | 放映厅 |
    // |   0  |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |  10  |  11  |  12  |   13   |
        let rscale;
        if (i>=8 && ratio[i]*100>=1) {
            let y2tmp = pie_y + rscales[i-1] * dy;
            // rscale = rscales[i-1];
            rscale = 1.2;
            while (vtx[i-1].y2 - y2tmp<20 && rscale<=3){
                rscale += 0.02;
                y2tmp = pie_y + rscale * dy;
            }
        } else {
            rscale = 1.2;
        }

        rscales[i] = rscale;
        // rscale = 1.15; //////////////////// Parameter
        let [x2,y2] = [pie_x+rscale*dx, pie_y+rscale*dy];

        let [x3,y3] = [x2+30*orient, y2];

        let tmp = {};
        [tmp.x1,tmp.y1] = [x1,y1];
        [tmp.x2,tmp.y2] = [x2,y2];
        [tmp.x3,tmp.y3] = [x3,y3];
        vtx[i] = tmp;
        orients[i] = orient;
    }

    // Disp labels
    for (let i=colnum-2; i>=0; i--){
        if (ratio[i]*100 < 1){
            continue;
        }
        block = blockarr[i];
        let orient = orients[i];

        let [x1,y1] = [vtx[i].x1, vtx[i].y1];
        let [x2,y2] = [vtx[i].x2, vtx[i].y2];
        let [x3,y3] = [vtx[i].x3, vtx[i].y3];
        push();
        noFill();
        colorMode(RGB,255);
        strokeWeight(1);
        stroke(block.r,block.g,block.b);

        stroke(block.r,block.g,block.b,0);
        beginShape();
        vertex(x1,y1);
        vertex(x2,y2);
        vertex(x3,y3);
        endShape();

        noStroke();
        fill(block.r,block.g,block.b);
        // console.log(orient);
        // textAlign((orient>0)?LEFT:RIGHT,CENTER);
        textAlign(CENTER,CENTER);
        textSize(16);
        // text(block.name,x3+orient*5,y3);
        text(block.name, x2+orient*5, y2);

        let name_width = textWidth(block.name);
        textAlign((orient>0)?LEFT:RIGHT,CENTER);
        // text(xround(ratio[i]*100,2)+'% ', x3+orient*(10+name_width), y3);
        text(xround(ratio[i]*100,1)+'% ', x2+orient*(10+name_width/2), y2);
        pop();
    }
}



function drawAxis(){
    let block_max = blockarr[sortedarr[0].id];
    let val_max = block_max.value;
    let str = val_max.toString();
    let unit = getUnit(str);
    let mark_max = num2mark(str);

    let max_floor = calcMaxFloor(val_max);

    // console.log(block_x,calcFloorCeil(val_max), val_max, block_max.w, block_w_bias);
    // console.log(mark_x,mark_y);

    let mark_count = parseInt(mark_max[0]);
    for (let i=1; i<=mark_count; i++){
        let mark_x, mark_y;
        mark_x = block_x + max_floor / val_max * block_max.w * (i/mark_count) + block_w_bias;
        mark_y = block_y_bias - 37;
        let mark_tmp = num2mark(max_floor* (i/mark_count));
        let mark_unit_tmp = mark_tmp + ' ' + unit;

        push();
        colorMode(RGB,255);
        noStroke();
        fill(255,255,255,90);
        textSize(18);
        textAlign(CENTER);
        text(mark_unit_tmp, mark_x, mark_y);
        stroke(255,255,255,60);
        // pop();
        // push();
        strokeWeight(2);
        line(mark_x,block_y_bias-20, mark_x, block_y_bias+blockarr.length*(block_h+block_gap));
        pop();
    }
    // return mark_unit;
}

/*function dispMaxVal(){
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
}*/

function saveFrame(title, count){
    let url = mycanvas.toDataURL('image/png');
    socket.emit('saveFrame', url, title, count);
}

function dispFrameRate(){
    let ratestr = format('{:>02d} FPS',floor(frameRate()));
    let cntstr = format('# {:>05d}',frameCount);
    colorMode(RGB,255);
    noStroke();
    // stroke(0,255,0);
    fill(0,255,0);
    textSize(15);
    text(ratestr,1100,100);
    text(cntstr,1170,100);
}

function dispDay(){
    let day = row.getString(0);
    colorMode(RGB,255);
    noStroke();
    // stroke(0,255,0);
    fill(0,255,0);
    textSize(15);
    text(day,1100,50);
}