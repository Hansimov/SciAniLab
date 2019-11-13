function bezier2d(pa1, pc1, pc2, pa2){
    // pa1 : anchor point 1
    // pc1 : control point 1
    // pc2 : control point 2
    // pa2 : anchor point 2
    bezier(pa1[0], pa1[1], pc1[0], pc1[1], pc2[0], pc2[1], pa2[0], pa2[1]);
}

function line2d(p1, p2){
    line(p1[0], p1[1], p2[0], p2[1]);
}



