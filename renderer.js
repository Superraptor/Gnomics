// renderer.js

const zerorpc = require("zerorpc");

var client = new zerorpc.Client(heartbeat=null, timeout=null, heartbeatInterval=10000000);

client.connect("tcp://127.0.0.1:4242");

client.invoke("echo", "server ready", (error, res) => {
    if(error || res !== 'server ready') {
        console.error(error);
    } else {
        console.log("Server is ready.");
    };
});