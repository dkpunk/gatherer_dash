var urlToImage = require('url-to-image');
 
var options = {
    width: 600,
    height: 800,
    // Give a short time to load additional resources
    requestTimeout: 100
}
 
urlToImage('https://splunk.yodlee.com/en-US/account/login?return_to=%2Fen-US%2F', 'google.png', options)
.then(function() {
    // do stuff with google.png
})
.catch(function(err) {
    console.error(err);
});
