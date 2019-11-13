require('./object-watch.js');

function Person(name='Alex',age=12){
    this.name= name;
    this.age = age;
    this.watch('name',Person.prototype.clog);
}


Person.prototype.clog = function (propname,oldval,newval){
    if (oldval != newval){
        console.log(newval);
    }
    return newval;
}

let bob = new Person('Bob',8);
bob.name = 'Bobb';
bob.name = 'Bobb';
bob.name = 'Bob';
