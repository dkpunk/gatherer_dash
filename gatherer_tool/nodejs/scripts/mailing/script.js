var nodemailer=require('nodemailer');
var transporter = nodemailer.createTransport({
service : 'gmail',
auth : {
 user : 'dinesh.tech1992@gmail.com',
pass : 'Pass@word1'
 },
tls : {
	rejectUnauthorized:false
}
});

var mailOptions  = {
from : 'dinesh.tech1992@gmail.com',
to : 'dinesh.heavymetal@gmail.com',
subject : 'Sending mail from node js',
text : 'Mail sent from server node'
};

transporter.sendMail(mailOptions,function(error,info){
if(error){
console.log(error);
}
else
{
console.log('Email sent:' + info.response);
}
});
