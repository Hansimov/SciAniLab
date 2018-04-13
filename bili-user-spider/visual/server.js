var express = require('express');
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var fs = require('fs');
var format = require('python-format')

app.use(express.static('.'));

app.get('/',function(req,res){
    res.sendFile(__dirname+'/index.html');
});

io.on('connection',function (socket){
    console.log('+ Refreshed!');

    socket.on('dataurl',function(url,frameCount){
        console.log(format('Saving Frame: {:>05d}',frameCount))
        var data = url.replace(/^data:image\/\w+;base64,/, "");
        var buf = new Buffer(data, 'base64');
        var img_name = format('./frames/frame_{:>05d}.png',frameCount)
        fs.writeFile(img_name, buf);
    });

});

http.listen(9100,function(){
    console.log('> Listening on port : 9100');
})