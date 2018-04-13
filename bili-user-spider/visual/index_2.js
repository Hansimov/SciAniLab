var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/',function(req,res){
    // res.send('<h1>Hello World</h1>');
    res.sendFile(__dirname+'/index.html');
});

io.on('connection',function(socket){
    console.log('Connected!');
    socket.on('disconnect',function(){
        console.log('Disconnected');
    });
    socket.on('chat',function(msg){
        console.log('message:' + msg);
        io.emit('chat',msg);
    });
})

http.listen(9100,function(){
    console.log('Listenning on : 9100');
});