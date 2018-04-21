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

function xround(num,n){
    let str = math.round(num,n).toString();
    let dot_index = str.indexOf('.');
    if (n>=1){
        if (dot_index<0){
            str = str + '.' + '0'.repeat(n);
        } else {
            str = str + '0'.repeat(dot_index+n+1-str.length);
        }
    }

    return str;
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
