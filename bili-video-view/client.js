let socket = io();
let videodata;
let blockarr = [];
let sortedarr =[];
let namearr = [];
let rgb =[];
let rownum, colnum;

let block_x = 100;
let block_h = 30;
let block_w_max = 700;
let block_w_bias = 1;

function preload(){
    // | 累计播放量 | 动画 | 番剧 | 国创 | 音乐 | 舞蹈 | 游戏 | 科技 | 生活 | 鬼畜 | 时尚 | 广告 | 娱乐 | 影视 | 放映厅 |
    // |      0     |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |  10  |  11  |  12  |  13  |   14   |

    videodata = loadTable('./videoviews.csv','csv');
}

function setup(){
    mycreatecanvas = createCanvas(1280,720);
    mycanvas = mycreatecanvas.canvas;
    background(0);
    frameRate(60);

    initBlocks();

    // noLoop();
}

function draw() {
    fc = frameCount;

    if (fc >= rownum-1){
        noLoop();
    }


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

Block = function(id=-1, name=""){
    this.id = id;
    this.name = name;

    this.value;

    this.rank;
    this.watch('rank',Block.prototype.updateRank);

    this.day;

    this.x;
    this.y;
    this.y_old;
    this.y_new;

    this.w;
    this.h;

    this.hue = hue;
    this.sat = 255;
    this.bri = 255;
    this.r;
    this.g;
    this.b;
    this.alp = 255;


    this.disp = function(){
        // this.move();
        // colorMode(HSB,255);
        colorMode(RGB,255);
        noStroke();
        // fill(this.hue,this.sat,this.bri,this.alp);
        fill(this.r, this.g, this.b, this.alp);
        rect(this.x,this.y, this.w,this.h);
        // console.log(this.x,this.y,this.w,this.h,this.hue);

        textAlign(RIGHT,CENTER);
        text(this.name,this.x-10,this.y+this.h/2);
        textAlign(LEFT,CENTER);
        text(this.value,this.x+this.w+10,this.y+this.h/2);
        textAlign(LEFT,CENTER);
        let nume_unit;
        if (this.value<=9999){
            nume_unit = '';
        } else {
            nume_unit = '( ' + num2unit(this.value) + ' )';
        }
        text(nume_unit,this.x+this.w+20+textWidth(this.value.toString()),this.y+this.h/2);
    };

    this.calcWidth = function(max, min){
        this.w = (this.value - min)/(max - min) * block_w_max + block_w_bias;
        // console.log(this.w);
    }

    this.rank2y = function(rank){
        let y = (rank+2)*40;
        return y;
    }

    this.movespeed = 0;
    this.moving = 0;

    this.move = function(){
        if (this.moving>0){
            // this.movespeed = (this.y_new-this.y_old)/80 
            //                  *(1+1/40*abs(abs(this.y-(this.y_new-this.y_old)/2)-(this.y_new-this.y_old)/2));
            this.y += this.movespeed;

            if ((this.y-this.y_new)*(this.y-this.y_old)>=0){
                this.y = this.y_new;
                this.moving = 0;
                this.alp = 255;
                this.movespeed = 0;
            }
        }
    }

}

Block.prototype.updateRank = function(propname, oldrank, newrank){
    if (oldrank!=newrank){
        this.y_old = this.y;
        this.y_new = this.rank2y(newrank);
        this.movespeed = (this.y_new-this.y_old)/25;
        this.moving = 1;
        this.alp = 255*0.7;
    }
    return newrank;
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
        block.y = 40*(i+2);
        block.w = 100;
        block.h = block_h;
        // block.hue = i/colnum*255;
        [block.r, block.g, block.b] = [255*rgbarr[i][0], 255*rgbarr[i][1], 255*rgbarr[i][2]];
        blockarr[i] = block;
    }

    // To make the first frame ordered
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
        ratio[i] = (blockarr[i].value+1)/totalnum;
    }
    let ang_bgn = 0;
    let ang_end;
    for (let i=0; i<colnum-1; i++){
        block = blockarr[i];
        ang_end = ang_bgn + 2*Math.PI*ratio[i];
        colorMode(RGB,255);
        stroke(255);
        fill(block.r, block.g, block.b);
        arc(1000,450,200,200,ang_bgn-Math.PI/2,ang_end-Math.PI/2,PIE);
        ang_bgn = ang_end;
    }


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

function num2unit(num){
    let str = num.toString();
    let len = str.length;
    let exp = len - 1;
    let mod = Math.floor(exp/4);

    let unit;
    if (mod==1){
        unit = '万';
    } else if (mod==2){
        unit = '亿';
    } else if (mod==3){
        unit = '万亿';
    } else {
        unit = '';
    }

    if (mod>=1 && mod<=3) {
        nume = str.slice(0,len-4*mod) + '.' + str.slice(len-4*mod,len-4*mod+2);
        nume = parseFloat(nume);

        let round_precision;
        if (exp<=mod*4+1) {
            round_precision = 1;
        } else {
            round_precision = 0;
        }

        nume = math.round(nume, round_precision).toString();
        // Since math.round() will convert 2.0 to 2,
        // I add the codes below to complement.
        if (nume.indexOf('.')<0){ 
            nume += '.0';
        }

        if (exp<=mod*4+1) {
            nume = nume.slice(0);
        } else {
            nume = nume.slice(0,-2);
        }
    } else {
        nume = str;
    }

    nume_unit = nume + ' ' + unit;
    return nume_unit;
}


function calcMaxCeil(val_max){
    let num_str = val_max.toString();
    let num_len = num_str.length;
    let num_head = num_str.slice(0, 2);
    let digits = [];
    digits[0] = parseInt(num_head[0]);
    digits[1] = parseInt(num_head[1]);
    if (digits[1]==9){
        if (digits[0]==9){
            digits[0] = 1;
            digits[1] = 0;
            num_len = num_len+1;
        } else {
            digits[1] = 0;
            digits[0] += 1;
        }
    } else{
        digits[1] +=1;
    }

    max_ceil = digits[0]*Math.pow(10,num_len-1)+digits[1]*Math.pow(10,num_len-2);

    return [num_len, digits, max_ceil];
}


function sortArray(){
    // sortedarr = [];
    for (let i=0; i<colnum-1; i++){
        let obj = {};
        obj.id = i;
        obj.val = parseInt(row.getString(i+1));
        sortedarr[i] = obj;
    }

    sortedarr = xmergeSort(sortedarr);
    sortedarr.reverse();
    // console.log(sortedarr);

    val_max = sortedarr[0].val;
    // let [num_len, digits, max_ceil] = calcMaxCeil(val_max);
    // val_min = sortedarr[sortedarr.length-1].val;
    let min = 0;

    // console.log(val_max,val_min);
    for (let i=0; i<colnum-1; i++){
        let id = sortedarr[i].id;
        blockarr[id].rank = i;
        blockarr[id].value = sortedarr[i].val;
        blockarr[id].calcWidth(val_max, min);
    }
}


function xmergeSort(arr) {
    if (arr.length <= 1) {
        return arr;
    }

    let midd = Math.floor(arr.length / 2);
    let arr_left = arr.slice(0, midd);
    let arr_righ = arr.slice(midd);

    return xmerge(xmergeSort(arr_left), xmergeSort(arr_righ));
}

function xmerge(arr_left, arr_righ) {
    let arr_sorted = [];
    let ptr_left = 0;
    let ptr_righ = 0;

    while (ptr_left < arr_left.length && ptr_righ < arr_righ.length) {
        if (arr_left[ptr_left].val < arr_righ[ptr_righ].val) {
            arr_sorted.push(arr_left[ptr_left]);
            ptr_left++;
        } else {
            arr_sorted.push(arr_righ[ptr_righ]);
            ptr_righ++;
        }
    }
    arr_sorted = arr_sorted.concat(arr_left.slice(ptr_left)).concat(arr_righ.slice(ptr_righ));
    return arr_sorted;
}

function saveFrame(){
    let dataurl = mycanvas.toDataURL('image/png');
    socket.emit('dataurl', dataurl, frameCount);
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