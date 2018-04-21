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
        let y = rank*(block_h + block_gap) + block_y_bias;
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
        this.movespeed = (this.y_new-this.y_old)/14;
        this.moving = 1;
        this.alp = 255*0.7;
    }
    return newrank;
}