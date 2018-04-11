var express = require('express');
 
app.use(express.bodyParser());
 
app.post('/', function(request, response){
  console.log(request.body.data);      
});