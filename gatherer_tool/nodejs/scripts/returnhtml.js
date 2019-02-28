var http = require('http');
var fs = require('fs');
http.createServer(function (req, res) {
  fs.readFile('/var/www/html/SO/SO/ToolOpsDashBoard/RETINS/MQ_scripts/DCS_UN_DASH/dinesh_test/Out_Network.html', function(err, data) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(data);
    res.end();
  });
}).listen(8080);
