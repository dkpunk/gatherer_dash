var events = require('events');
var eventEmitter = new events.EventEmitter();
var myEventHandler = function() {
console.log('I Hear a screa,!');
}

eventEmitter.on('scream',myEventHandler);
eventEmitter.emit('scream');
