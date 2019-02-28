var fs = require('fs');

fs.open('textfileappend.txt','w',function (err,file) {
if (err) throw err;
console.log('Saved!');
});
