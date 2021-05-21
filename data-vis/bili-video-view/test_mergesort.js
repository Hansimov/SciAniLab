function mergeSort(arr) {
    if (arr.length <= 1) {
        return arr;
    }

    let midd = Math.floor(arr.length / 2);
    let arr_left = arr.slice(0, midd);
    let arr_righ = arr.slice(midd);

    return merge(mergeSort(arr_left), mergeSort(arr_righ));
}

function merge(arr_left, arr_righ) {
    let arr_sorted = [];
    let ptr_left = 0;
    let ptr_righ = 0;

    while (ptr_left < arr_left.length && ptr_righ < arr_righ.length) {
        if (arr_left[ptr_left] < arr_righ[ptr_righ]) {
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

let samparr = [1,5,9,3,7,2,8,4,6,0];
let myarr = new Array(samparr.length);
// console.log(mergeSort(samparr));

for (let i=0; i<samparr.length;i++){
    let tmp = {};
    tmp.idx = i;
    tmp.val = samparr[i];
    myarr[i] = tmp;
}
console.log(myarr);
myarr_sorted = xmergeSort(myarr)
console.log(myarr_sorted);
let idx = [];
for (let i=0;i<myarr_sorted.length;i++){
    idx[i] = myarr_sorted[i].idx;
}
console.log(idx);


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








// https://stackoverflow.com/questions/3730510/javascript-sort-array-and-return-an-array-of-indicies-that-indicates-the-positi

// function sortWithIndeces(toSort) {
//   for (var i = 0; i < toSort.length; i++) {
//     toSort[i] = [toSort[i], i];
//   }
//   toSort.sort(function(left, right) {
//     return left[0] < right[0] ? -1 : 1;
//   });
//   toSort.sortIndices = [];
//   for (var j = 0; j < toSort.length; j++) {
//     toSort.sortIndices.push(toSort[j][1]);
//     toSort[j] = toSort[j][0];
//   }
//   return toSort;
// }

// var test = ['b', 'c', 'd', 'a'];
// sortWithIndeces(test);
// console.log(test.sortIndices.join(","));