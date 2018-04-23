let express = require('express');
let app = express();
let server = require('http').Server(app);
let io = require('socket.io')(server);
let fs = require('fs');
let format = require('python-format');
let reload = require('reload');
let mkdirp = require('mkdirp');

// Stop-Process -Id (Get-NetTCPConnection -LocalPort 9100).OwningProcess -Force

app.use(express.static('.'));

app.get('/',function(req,res){
    res.sendFile(__dirname+'/index.html');
});

io.on('connection',function (socket){
    console.log('+ Refreshed!');
    socket.on('disconnect',function(){
        console.log('- Disconnected!');
    });

    socket.on('saveFrame',function(url, title, count){
        console.log(format('Saving Frame: {:>05d}',count))
        var data = url.replace(/^data:image\/\w+;base64,/, "");
        var buf = new Buffer(data, 'base64');
        // console.log('./frames/' + title);

        // mkdirp('./frames');
        // mkdirp('./frames/' + title);
        var img_name = format('./frames/{0}/{0}_{1:>05d}.png', title, count)
        fs.writeFile(img_name, buf);
    });
});

server.listen(9100,function(){
    console.log('> Listening on port : 9100');
});

reload(app);